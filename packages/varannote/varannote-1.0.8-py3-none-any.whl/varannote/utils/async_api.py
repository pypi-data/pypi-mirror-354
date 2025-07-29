#!/usr/bin/env python3
"""
Async API System for VarAnnote v1.0.0

Provides asynchronous API calls for parallel database queries:
- aiohttp integration for concurrent requests
- Rate limiting and retry mechanisms
- Connection pooling and session management
- Error handling and fallback strategies
- Performance optimization for large datasets
"""

import asyncio
import aiohttp
import time
import json
from typing import Dict, List, Any, Optional, Union, Callable, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging
from contextlib import asynccontextmanager
import ssl
import certifi

from .logger import get_logger


@dataclass
class APIConfig:
    """Configuration for API endpoints"""
    name: str
    base_url: str
    rate_limit: float  # requests per second
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    requires_auth: bool = False
    auth_header: Optional[str] = None
    api_key: Optional[str] = None
    priority: int = 5


@dataclass
class APIRequest:
    """Individual API request"""
    url: str
    method: str = "GET"
    params: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None
    timeout: Optional[int] = None
    variant_id: Optional[str] = None
    database: Optional[str] = None


@dataclass
class APIResponse:
    """API response wrapper"""
    success: bool
    status_code: Optional[int] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration: float = 0.0
    variant_id: Optional[str] = None
    database: Optional[str] = None
    retries: int = 0


class RateLimiter:
    """Rate limiter for API calls"""
    
    def __init__(self, rate_limit: float):
        """
        Initialize rate limiter
        
        Args:
            rate_limit: Maximum requests per second
        """
        self.rate_limit = rate_limit
        self.min_interval = 1.0 / rate_limit if rate_limit > 0 else 0
        self.last_call = 0.0
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire rate limit token"""
        async with self._lock:
            now = time.time()
            time_since_last = now - self.last_call
            
            if time_since_last < self.min_interval:
                sleep_time = self.min_interval - time_since_last
                await asyncio.sleep(sleep_time)
            
            self.last_call = time.time()


class AsyncAPIClient:
    """
    Asynchronous API client for VarAnnote
    
    Features:
    - Concurrent API requests with aiohttp
    - Rate limiting per API endpoint
    - Automatic retries with exponential backoff
    - Connection pooling and session management
    - SSL verification and certificate handling
    - Request/response logging and metrics
    """
    
    def __init__(self, 
                 max_connections: int = 100,
                 max_connections_per_host: int = 30,
                 enable_ssl_verification: bool = True,
                 user_agent: str = "VarAnnote/1.0.0"):
        """
        Initialize async API client
        
        Args:
            max_connections: Maximum total connections
            max_connections_per_host: Maximum connections per host
            enable_ssl_verification: Enable SSL certificate verification
            user_agent: User agent string for requests
        """
        self.logger = get_logger("async_api")
        self.max_connections = max_connections
        self.max_connections_per_host = max_connections_per_host
        self.enable_ssl_verification = enable_ssl_verification
        self.user_agent = user_agent
        
        # API configurations
        self.api_configs: Dict[str, APIConfig] = {}
        
        # Rate limiters per API
        self.rate_limiters: Dict[str, RateLimiter] = {}
        
        # Session and connector
        self.session: Optional[aiohttp.ClientSession] = None
        self.connector: Optional[aiohttp.TCPConnector] = None
        
        # Metrics
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'total_duration': 0.0,
            'api_stats': {}
        }
    
    def add_api_config(self, config: APIConfig):
        """Add API configuration"""
        self.api_configs[config.name] = config
        self.rate_limiters[config.name] = RateLimiter(config.rate_limit)
        
        # Initialize API stats
        self.metrics['api_stats'][config.name] = {
            'requests': 0,
            'successes': 0,
            'failures': 0,
            'total_duration': 0.0,
            'avg_duration': 0.0
        }
        
        self.logger.info(f"Added API config: {config.name} - {config.base_url}")
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self._create_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self._close_session()
    
    async def _create_session(self):
        """Create aiohttp session with optimized settings"""
        # SSL context
        if self.enable_ssl_verification:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
        else:
            ssl_context = False
        
        # Connection limits
        connector = aiohttp.TCPConnector(
            limit=self.max_connections,
            limit_per_host=self.max_connections_per_host,
            ssl=ssl_context,
            enable_cleanup_closed=True,
            keepalive_timeout=30,
            ttl_dns_cache=300
        )
        
        # Default headers
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate'
        }
        
        # Timeout configuration
        timeout = aiohttp.ClientTimeout(
            total=60,
            connect=10,
            sock_read=30
        )
        
        self.connector = connector
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers=headers,
            timeout=timeout,
            raise_for_status=False
        )
        
        self.logger.info("Async API session created")
    
    async def _close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
        
        if self.connector:
            await self.connector.close()
            self.connector = None
        
        self.logger.info("Async API session closed")
    
    async def make_request(self, 
                          api_name: str, 
                          request: APIRequest) -> APIResponse:
        """
        Make single API request
        
        Args:
            api_name: Name of API configuration
            request: API request details
            
        Returns:
            API response
        """
        if api_name not in self.api_configs:
            return APIResponse(
                success=False,
                error=f"Unknown API: {api_name}",
                variant_id=request.variant_id,
                database=request.database
            )
        
        config = self.api_configs[api_name]
        
        # Apply rate limiting
        await self.rate_limiters[api_name].acquire()
        
        # Prepare request
        url = request.url
        if not url.startswith('http'):
            url = f"{config.base_url.rstrip('/')}/{url.lstrip('/')}"
        
        headers = dict(request.headers or {})
        
        # Add authentication if required
        if config.requires_auth and config.api_key:
            if config.auth_header:
                headers[config.auth_header] = config.api_key
            else:
                headers['Authorization'] = f"Bearer {config.api_key}"
        
        timeout = request.timeout or config.timeout
        
        # Make request with retries
        start_time = time.time()
        response = await self._make_request_with_retries(
            config, url, request.method, request.params, 
            request.data, headers, timeout
        )
        duration = time.time() - start_time
        
        # Update metrics
        self._update_metrics(api_name, response.success, duration)
        
        response.duration = duration
        response.variant_id = request.variant_id
        response.database = request.database
        
        return response
    
    async def _make_request_with_retries(self,
                                       config: APIConfig,
                                       url: str,
                                       method: str,
                                       params: Optional[Dict[str, Any]],
                                       data: Optional[Dict[str, Any]],
                                       headers: Dict[str, str],
                                       timeout: int) -> APIResponse:
        """Make request with retry logic"""
        last_error = None
        
        for attempt in range(config.max_retries + 1):
            try:
                async with self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as response:
                    
                    # Check for rate limiting
                    if response.status == 429:
                        retry_after = int(response.headers.get('Retry-After', config.retry_delay))
                        self.logger.warning(f"Rate limited by {config.name}, waiting {retry_after}s")
                        await asyncio.sleep(retry_after)
                        continue
                    
                    # Parse response
                    try:
                        response_data = await response.json()
                    except (aiohttp.ContentTypeError, json.JSONDecodeError):
                        response_data = await response.text()
                    
                    if response.status < 400:
                        return APIResponse(
                            success=True,
                            status_code=response.status,
                            data=response_data,
                            retries=attempt
                        )
                    else:
                        error_msg = f"HTTP {response.status}: {response_data}"
                        if attempt < config.max_retries:
                            self.logger.warning(f"Request failed (attempt {attempt + 1}): {error_msg}")
                            await asyncio.sleep(config.retry_delay * (2 ** attempt))
                            continue
                        else:
                            return APIResponse(
                                success=False,
                                status_code=response.status,
                                error=error_msg,
                                retries=attempt
                            )
            
            except asyncio.TimeoutError:
                last_error = "Request timeout"
                if attempt < config.max_retries:
                    self.logger.warning(f"Timeout (attempt {attempt + 1}), retrying...")
                    await asyncio.sleep(config.retry_delay * (2 ** attempt))
                    continue
            
            except Exception as e:
                last_error = str(e)
                if attempt < config.max_retries:
                    self.logger.warning(f"Request error (attempt {attempt + 1}): {e}")
                    await asyncio.sleep(config.retry_delay * (2 ** attempt))
                    continue
        
        return APIResponse(
            success=False,
            error=last_error or "Max retries exceeded",
            retries=config.max_retries
        )
    
    async def make_batch_requests(self, 
                                 requests: List[Tuple[str, APIRequest]],
                                 max_concurrent: int = 50) -> List[APIResponse]:
        """
        Make batch of API requests concurrently
        
        Args:
            requests: List of (api_name, request) tuples
            max_concurrent: Maximum concurrent requests
            
        Returns:
            List of API responses
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def bounded_request(api_name: str, request: APIRequest) -> APIResponse:
            async with semaphore:
                return await self.make_request(api_name, request)
        
        self.logger.info(f"Making {len(requests)} batch requests with max_concurrent={max_concurrent}")
        
        with self.logger.operation_timer("batch_api_requests", request_count=len(requests)):
            tasks = [
                bounded_request(api_name, request)
                for api_name, request in requests
            ]
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle exceptions
            processed_responses = []
            for i, response in enumerate(responses):
                if isinstance(response, Exception):
                    api_name, request = requests[i]
                    processed_responses.append(APIResponse(
                        success=False,
                        error=str(response),
                        variant_id=request.variant_id,
                        database=request.database
                    ))
                else:
                    processed_responses.append(response)
        
        successful = sum(1 for r in processed_responses if r.success)
        self.logger.info(f"Batch requests completed: {successful}/{len(requests)} successful")
        
        return processed_responses
    
    def _update_metrics(self, api_name: str, success: bool, duration: float):
        """Update API metrics"""
        self.metrics['total_requests'] += 1
        self.metrics['total_duration'] += duration
        
        if success:
            self.metrics['successful_requests'] += 1
        else:
            self.metrics['failed_requests'] += 1
        
        # API-specific metrics
        api_stats = self.metrics['api_stats'][api_name]
        api_stats['requests'] += 1
        api_stats['total_duration'] += duration
        
        if success:
            api_stats['successes'] += 1
        else:
            api_stats['failures'] += 1
        
        # Update average duration
        api_stats['avg_duration'] = api_stats['total_duration'] / api_stats['requests']
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get API metrics summary"""
        total_requests = self.metrics['total_requests']
        
        if total_requests == 0:
            return {'message': 'No requests made yet'}
        
        success_rate = (self.metrics['successful_requests'] / total_requests) * 100
        avg_duration = self.metrics['total_duration'] / total_requests
        
        return {
            'total_requests': total_requests,
            'successful_requests': self.metrics['successful_requests'],
            'failed_requests': self.metrics['failed_requests'],
            'success_rate': round(success_rate, 2),
            'average_duration': round(avg_duration, 3),
            'total_duration': round(self.metrics['total_duration'], 3),
            'api_breakdown': dict(self.metrics['api_stats'])
        }
    
    def log_metrics_summary(self):
        """Log metrics summary"""
        summary = self.get_metrics_summary()
        
        if 'message' in summary:
            self.logger.info(summary['message'])
            return
        
        self.logger.info("=== Async API Metrics Summary ===")
        self.logger.info(f"Total requests: {summary['total_requests']}")
        self.logger.info(f"Success rate: {summary['success_rate']}%")
        self.logger.info(f"Average duration: {summary['average_duration']}s")
        
        for api_name, stats in summary['api_breakdown'].items():
            if stats['requests'] > 0:
                api_success_rate = (stats['successes'] / stats['requests']) * 100
                self.logger.info(f"  {api_name}: {stats['requests']} requests, "
                               f"{api_success_rate:.1f}% success, "
                               f"{stats['avg_duration']:.3f}s avg")


class AsyncDatabaseClient:
    """
    Async client for database API calls
    
    Specialized for VarAnnote database queries with:
    - Pre-configured database endpoints
    - Variant-specific request formatting
    - Response parsing and normalization
    - Fallback and error handling
    """
    
    def __init__(self, api_client: AsyncAPIClient):
        """
        Initialize async database client
        
        Args:
            api_client: Async API client instance
        """
        self.api_client = api_client
        self.logger = get_logger("async_db")
        
        # Configure database APIs
        self._setup_database_apis()
    
    def _setup_database_apis(self):
        """Set up database API configurations"""
        database_configs = [
            APIConfig(
                name="clinvar",
                base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
                rate_limit=3.0,  # 3 requests per second
                timeout=30,
                priority=12
            ),
            APIConfig(
                name="gnomad",
                base_url="https://gnomad.broadinstitute.org/api",
                rate_limit=2.0,  # 2 requests per second
                timeout=45,
                priority=6
            ),
            APIConfig(
                name="dbsnp",
                base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
                rate_limit=3.0,
                timeout=30,
                priority=4
            ),
            APIConfig(
                name="ensembl",
                base_url="https://rest.ensembl.org",
                rate_limit=15.0,  # 15 requests per second
                timeout=30,
                priority=8
            )
        ]
        
        for config in database_configs:
            self.api_client.add_api_config(config)
    
    async def query_variant_batch(self, 
                                 variants: List[Dict[str, Any]],
                                 databases: Optional[List[str]] = None,
                                 max_concurrent: int = 30) -> Dict[str, List[APIResponse]]:
        """
        Query multiple variants across multiple databases
        
        Args:
            variants: List of variant dictionaries
            databases: List of database names to query
            max_concurrent: Maximum concurrent requests
            
        Returns:
            Dictionary mapping database names to response lists
        """
        if databases is None:
            databases = list(self.api_client.api_configs.keys())
        
        # Build requests
        requests = []
        for variant in variants:
            variant_id = variant.get('variant_id', f"{variant['CHROM']}:{variant['POS']}:{variant['REF']}>{variant['ALT']}")
            
            for db_name in databases:
                request = self._build_database_request(db_name, variant)
                if request:
                    request.variant_id = variant_id
                    request.database = db_name
                    requests.append((db_name, request))
        
        self.logger.info(f"Querying {len(variants)} variants across {len(databases)} databases")
        
        # Make batch requests
        responses = await self.api_client.make_batch_requests(requests, max_concurrent)
        
        # Group responses by database
        results = {db_name: [] for db_name in databases}
        for response in responses:
            if response.database:
                results[response.database].append(response)
        
        return results
    
    def _build_database_request(self, db_name: str, variant: Dict[str, Any]) -> Optional[APIRequest]:
        """Build database-specific API request"""
        if db_name == "clinvar":
            return self._build_clinvar_request(variant)
        elif db_name == "gnomad":
            return self._build_gnomad_request(variant)
        elif db_name == "dbsnp":
            return self._build_dbsnp_request(variant)
        elif db_name == "ensembl":
            return self._build_ensembl_request(variant)
        else:
            return None
    
    def _build_clinvar_request(self, variant: Dict[str, Any]) -> APIRequest:
        """Build ClinVar API request"""
        chrom = variant['CHROM'].replace('chr', '')
        pos = variant['POS']
        
        params = {
            'db': 'clinvar',
            'term': f'{chrom}[chr] AND {pos}[chrpos]',
            'retmode': 'json',
            'retmax': 10
        }
        
        return APIRequest(
            url="esearch.fcgi",
            params=params
        )
    
    def _build_gnomad_request(self, variant: Dict[str, Any]) -> APIRequest:
        """Build gnomAD API request"""
        chrom = variant['CHROM'].replace('chr', '')
        pos = variant['POS']
        ref = variant['REF']
        alt = variant['ALT']
        
        # GraphQL query for gnomAD v4
        query = {
            'query': '''
            query VariantQuery($variantId: String!) {
                variant(variantId: $variantId, dataset: gnomad_r4) {
                    variantId
                    genome {
                        ac
                        an
                        af
                        populations {
                            id
                            ac
                            an
                            af
                        }
                    }
                }
            }
            ''',
            'variables': {
                'variantId': f'{chrom}-{pos}-{ref}-{alt}'
            }
        }
        
        return APIRequest(
            url="",
            method="POST",
            data=query,
            headers={'Content-Type': 'application/json'}
        )
    
    def _build_dbsnp_request(self, variant: Dict[str, Any]) -> APIRequest:
        """Build dbSNP API request"""
        chrom = variant['CHROM'].replace('chr', '')
        pos = variant['POS']
        
        params = {
            'db': 'snp',
            'term': f'{chrom}[chr] AND {pos}[chrpos]',
            'retmode': 'json',
            'retmax': 5
        }
        
        return APIRequest(
            url="esearch.fcgi",
            params=params
        )
    
    def _build_ensembl_request(self, variant: Dict[str, Any]) -> APIRequest:
        """Build Ensembl API request"""
        chrom = variant['CHROM'].replace('chr', '')
        pos = variant['POS']
        ref = variant['REF']
        alt = variant['ALT']
        
        # VEP (Variant Effect Predictor) endpoint
        variant_notation = f"{chrom}:{pos}:{ref}/{alt}"
        
        return APIRequest(
            url=f"vep/human/hgvs/{variant_notation}",
            params={'content-type': 'application/json'}
        )


# Convenience functions
async def create_async_client(**kwargs) -> AsyncAPIClient:
    """Create and initialize async API client"""
    client = AsyncAPIClient(**kwargs)
    await client._create_session()
    return client


@asynccontextmanager
async def async_api_session(**kwargs):
    """Async context manager for API session"""
    async with AsyncAPIClient(**kwargs) as client:
        yield client


# Example usage function
async def example_usage():
    """Example of how to use the async API system"""
    logger = get_logger("example")
    
    # Sample variants
    variants = [
        {'CHROM': '17', 'POS': 43044295, 'REF': 'G', 'ALT': 'A'},
        {'CHROM': '1', 'POS': 100, 'REF': 'A', 'ALT': 'T'},
        {'CHROM': '2', 'POS': 200, 'REF': 'G', 'ALT': 'C'}
    ]
    
    async with async_api_session() as api_client:
        db_client = AsyncDatabaseClient(api_client)
        
        # Query variants
        results = await db_client.query_variant_batch(
            variants=variants,
            databases=['clinvar', 'ensembl'],
            max_concurrent=10
        )
        
        # Log results
        for db_name, responses in results.items():
            successful = sum(1 for r in responses if r.success)
            logger.info(f"{db_name}: {successful}/{len(responses)} successful")
        
        # Show metrics
        api_client.log_metrics_summary()


if __name__ == "__main__":
    asyncio.run(example_usage()) 