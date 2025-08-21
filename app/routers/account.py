from fastapi import APIRouter, HTTPException

from app.core.schwab_client import get_schwab_client

router = APIRouter(prefix="/account", tags=["account"])


@router.get("/")
async def get_account_info():
    """Get account information"""
    schwab_client = get_schwab_client()
    if not schwab_client:
        raise HTTPException(status_code=500, detail="Schwab client not initialized")

    try:
        account_info = schwab_client.get_account_numbers()
        return {"accounts": account_info.json()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching account info: {e!s}"
        ) from e


@router.get("/details")
async def get_account_details():
    """Get detailed account information"""
    schwab_client = get_schwab_client()
    if not schwab_client:
        raise HTTPException(status_code=500, detail="Schwab client not initialized")

    try:
        account_info = schwab_client.get_account_numbers()
        accounts = account_info.json()

        # Get detailed info for each account
        detailed_accounts = []
        for account in accounts:
            account_hash = account["hashValue"]
            account_detail = schwab_client.get_account(account_hash)
            detailed_accounts.append(account_detail.json())

        return {"accounts": detailed_accounts}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching account details: {e!s}"
        ) from e


@router.get("/balances")
async def get_account_balances():
    """Get account balances"""
    schwab_client = get_schwab_client()
    if not schwab_client:
        raise HTTPException(status_code=500, detail="Schwab client not initialized")

    try:
        account_info = schwab_client.get_account_numbers()
        accounts = account_info.json()

        balances = []
        for account in accounts:
            account_hash = account["hashValue"]
            account_detail = schwab_client.get_account(account_hash)
            account_data = account_detail.json()

            # Extract balance information
            balance_info = {
                "accountNumber": account["accountNumber"],
                "hashValue": account_hash,
                "balances": account_data.get("securitiesAccount", {}).get(
                    "currentBalances", {}
                ),
            }
            balances.append(balance_info)

        return {"balances": balances}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching account balances: {e!s}"
        ) from e
