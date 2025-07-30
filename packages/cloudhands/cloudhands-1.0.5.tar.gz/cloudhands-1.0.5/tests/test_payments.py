import os
from src.cloudhands import CloudHandsPayment
from dotenv import load_dotenv

load_dotenv()

def main():
    author_key = os.getenv("AUTHOR_KEY")
    chPay = CloudHandsPayment(
        author_key=author_key,
    )
    
    chPay.cli_authorize()

    print("CloudHands SDK initialized.")
    print("SDK values:", chPay.__dict__ )
    # Charge usage.
    result = chPay.charge(
        charge=1,
        event_name="PYTHON SDK DEMO",
    )

    print("Charge result:", result.__dict__)
    if result.is_successful:
        print("Usage event posted successfully!")
        print("getting transaction for transaction_id:", result.transaction_id)
        transaction = chPay.get_transaction(result.transaction_id)
        print("Transaction details:", transaction.__dict__)
    else:
        print("Failed to post usage event.")
        if result.errors:
            print("Errors:", result.errors)

if __name__ == "__main__":
    main()

