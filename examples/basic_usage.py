"""
Example: Basic Usage of TrackHS MCP Connector

This example demonstrates basic MCP operations with the TrackHS connector.
Shows how to search reservations using the Clean Architecture implementation.
"""

import asyncio
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.trackhs_mcp.application.use_cases.search_reservations import (
    SearchReservationsUseCase,
)
from src.trackhs_mcp.infrastructure.adapters.config import TrackHSConfig
from src.trackhs_mcp.infrastructure.adapters.trackhs_api_client import TrackHSApiClient


async def main():
    """Basic usage example"""

    print("TrackHS MCP Connector - Basic Usage Example")
    print("=" * 50)

    try:
        # 1. Configure the client
        print("1. Configuring TrackHS client...")
        config = TrackHSConfig.from_env()
        api_client = TrackHSApiClient(config)
        print(f"   ✓ Connected to: {config.base_url}")

        # 2. Create use case
        print("2. Creating search use case...")
        search_use_case = SearchReservationsUseCase(api_client)
        print("   ✓ Use case created")

        # 3. Search reservations with basic filters
        print("3. Searching reservations...")
        filters = {
            'date_from': '2024-01-01',
            'date_to': '2024-01-31',
            'status': 'confirmed',
            'per_page': 10
        }

        result = await search_use_case.execute(filters)

        print(f"   ✓ Found {result['total']} reservations")

        # 4. Display results
        print("\n4. Reservation Results:")
        print("-" * 30)

        if result['reservations']:
            for i, reservation in enumerate(result['reservations'][:5], 1):
                print(f"{i}. {reservation.guest_name}")
                print(f"   Arrival: {reservation.arrival_date}")
                print(f"   Departure: {reservation.departure_date}")
                print(f"   Status: {reservation.status}")
                print(f"   Amount: ${reservation.total_amount}")
                print()

            if len(result['reservations']) > 5:
                print(f"... and {len(result['reservations']) - 5} more reservations")
        else:
            print("No reservations found for the specified criteria")

        # 5. Show pagination info
        if 'pagination' in result:
            pagination = result['pagination']
            print(f"\nPagination Info:")
            print(f"  Current page: {pagination.get('current_page', 'N/A')}")
            print(f"  Total pages: {pagination.get('total_pages', 'N/A')}")
            print(f"  Items per page: {pagination.get('per_page', 'N/A')}")

        # 6. Test advanced search
        print("\n5. Testing advanced search...")
        advanced_filters = {
            'date_from': '2024-01-01',
            'date_to': '2024-12-31',
            'status': 'confirmed',
            'sort_by': 'arrival_date',
            'sort_order': 'asc',
            'per_page': 5
        }

        advanced_result = await search_use_case.execute(advanced_filters)
        print(f"   ✓ Advanced search found {advanced_result['total']} reservations")

        # 7. Clean up
        print("\n6. Cleaning up...")
        await api_client.close()
        print("   ✓ Connection closed")

        print("\n" + "=" * 50)
        print("Example completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your .env file configuration")
        print("2. Verify Track HS API credentials")
        print("3. Ensure network connectivity")
        print("4. Check API endpoint availability")

def check_environment():
    """Check if environment is properly configured"""
    print("Environment Check:")
    print("-" * 20)

    required_vars = ['TRACKHS_API_URL', 'TRACKHS_USERNAME', 'TRACKHS_PASSWORD']

    for var in required_vars:
        value = os.getenv(var)
        if value:
            if var == 'TRACKHS_PASSWORD':
                print(f"✓ {var}: {'*' * len(value)}")
            else:
                print(f"✓ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")

    print()

if __name__ == "__main__":
    print("TrackHS MCP Connector - Basic Usage Example")
    print("=" * 50)

    # Check environment
    check_environment()

    # Run the example
    asyncio.run(main())
