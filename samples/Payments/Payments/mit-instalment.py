from CyberSource import *
import os
import json
from importlib.machinery import SourceFileLoader
from pathlib import Path

config_file = os.path.join(os.getcwd(), "data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()

# To delete None values in Input Request Json body
def del_none(d):
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
        elif isinstance(value, list):
            for item in value:
                del_none(item)
    return d

def mit_instalment():
    clientReferenceInformationCode = "TC50171_3"
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code = clientReferenceInformationCode
    )

    processingInformationCapture = False
    processingInformationCommerceIndicator = "install"
    processingInformationAuthorizationOptionsIgnoreAvsResult = False
    processingInformationAuthorizationOptionsIgnoreCvResult = False
    processingInformationAuthorizationOptionsInitiatorType = "merchant"
    processingInformationAuthorizationOptionsInitiatorStoredCredentialUsed = True
    processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionPreviousTransactionId = "123456789012345"
    processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction = Ptsv2paymentsProcessingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction(
        previous_transaction_id = processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransactionPreviousTransactionId
    )

    processingInformationAuthorizationOptionsInitiator = Ptsv2paymentsProcessingInformationAuthorizationOptionsInitiator(
        type = processingInformationAuthorizationOptionsInitiatorType,
        stored_credential_used = processingInformationAuthorizationOptionsInitiatorStoredCredentialUsed,
        merchant_initiated_transaction = processingInformationAuthorizationOptionsInitiatorMerchantInitiatedTransaction.__dict__
    )

    processingInformationAuthorizationOptions = Ptsv2paymentsProcessingInformationAuthorizationOptions(
        ignore_avs_result = processingInformationAuthorizationOptionsIgnoreAvsResult,
        ignore_cv_result = processingInformationAuthorizationOptionsIgnoreCvResult,
        initiator = processingInformationAuthorizationOptionsInitiator.__dict__
    )

    processingInformation = Ptsv2paymentsProcessingInformation(
        capture = processingInformationCapture,
        commerce_indicator = processingInformationCommerceIndicator,
        authorization_options = processingInformationAuthorizationOptions.__dict__
    )

    paymentInformationCardNumber = "4111111111111111"
    paymentInformationCardExpirationMonth = "12"
    paymentInformationCardExpirationYear = "2031"
    paymentInformationCardType = "001"
    paymentInformationCard = Ptsv2paymentsPaymentInformationCard(
        number = paymentInformationCardNumber,
        expiration_month = paymentInformationCardExpirationMonth,
        expiration_year = paymentInformationCardExpirationYear,
        type = paymentInformationCardType
    )

    paymentInformation = Ptsv2paymentsPaymentInformation(
        card = paymentInformationCard.__dict__
    )

    orderInformationAmountDetailsTotalAmount = "102.21"
    orderInformationAmountDetailsCurrency = "GBP"
    orderInformationAmountDetails = Ptsv2paymentsOrderInformationAmountDetails(
        total_amount = orderInformationAmountDetailsTotalAmount,
        currency = orderInformationAmountDetailsCurrency
    )

    orderInformationBillToFirstName = "John"
    orderInformationBillToLastName = "Doe"
    orderInformationBillToAddress1 = "1 Market St"
    orderInformationBillToLocality = "san francisco"
    orderInformationBillToAdministrativeArea = "CA"
    orderInformationBillToPostalCode = "94105"
    orderInformationBillToCountry = "US"
    orderInformationBillToEmail = "test@cybs.com"
    orderInformationBillToPhoneNumber = "4158880000"
    orderInformationBillTo = Ptsv2paymentsOrderInformationBillTo(
        first_name = orderInformationBillToFirstName,
        last_name = orderInformationBillToLastName,
        address1 = orderInformationBillToAddress1,
        locality = orderInformationBillToLocality,
        administrative_area = orderInformationBillToAdministrativeArea,
        postal_code = orderInformationBillToPostalCode,
        country = orderInformationBillToCountry,
        email = orderInformationBillToEmail,
        phone_number = orderInformationBillToPhoneNumber
    )

    orderInformation = Ptsv2paymentsOrderInformation(
        amount_details = orderInformationAmountDetails.__dict__,
        bill_to = orderInformationBillTo.__dict__
    )

    requestObj = CreatePaymentRequest(
        client_reference_information = clientReferenceInformation.__dict__,
        processing_information = processingInformation.__dict__,
        payment_information = paymentInformation.__dict__,
        order_information = orderInformation.__dict__
    )


    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)


    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = PaymentsApi(client_config)
        return_data, status, body = api_instance.create_payment(requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)

        write_log_audit(status)

        return return_data
    except Exception as e:
        write_log_audit(e.status)
        print("\nException when calling PaymentsApi->create_payment: %s\n" % e)

def write_log_audit(status):
    print(f"[Sample Code Testing] [{Path(__file__).stem}] {status}")

if __name__ == "__main__":
    mit_instalment()