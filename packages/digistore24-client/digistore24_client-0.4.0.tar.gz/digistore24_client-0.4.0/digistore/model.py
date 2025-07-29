import dataclasses
import enum
import typing


parsable_to_int = str
parsable_to_float = str


class DigiBool(enum.StrEnum):
    TRUE = 'Y'
    ALWAYS = 'Y_always'
    FALSE = 'N'
    HIDDEN = 'hidden'
    NONE = ''


class ResultStatus(enum.StrEnum):
    SUCCESS = 'success'
    ERROR = 'error'


class ApprovalStatus(enum.StrEnum):
    NEW = 'new'
    PENDING = 'pending'


class BuyerType(enum.StrEnum):
    CONSUMER = 'consumer'
    BUSINESS = 'business'


class ProductType(enum.StrEnum):
    '''
    retrieved from getGlobalSettings (product_types attr)
    '''
    DOWNLOADS = '1'
    ON_SITE_SERVICE = '13'
    SEMINAR_OR_EVENT_FOR_RECREATION = '15'
    SOFTWARE = '37'
    MEMBER_AREA_AND_VIDEO_COURSES = '38'
    DELIVERABLE = '4'
    EBOOKS = '42'
    AUDIOBOOK_DOWNLOAD = '44'
    WEBINAR = '45'
    ONLINE_COACHING = '46'
    TELEPHONE_COACHING = '50'
    REMOTE_SERVICE_PROVIDED_ELECTRONICALLY = '7'


@dataclasses.dataclass(kw_only=True)
class Response:
    '''
    wrapper for responses returned by digistore-api-calls
    '''
    api_version: str
    current_time: str
    timezone: str
    utc_offset: int
    result: ResultStatus
    message: str | None = None
    runtime_seconds: float = None
    data: dict = dataclasses.field(default_factory=dict) # only populated if successful

    @property
    def successful(self) -> bool:
        return self.result is ResultStatus.SUCCESS


@dataclasses.dataclass(kw_only=True)
class ShortProduct:
    '''
    dataclass to use for creating new products (createProduct route) or altering existing ones.

    Contains all documented attributes (less than existing products retrieve from digistore have),
    with the notable exception of language-specific names (name_de, name_es, ..)

    All attributes are according to documentation, optional. Attribute order reflects order from
    digistore's documentation, but is (likely)  not relevant.
    '''
    name: str
    name_intern: str | None = None
    description: str | None = None # html
    salespage_url: str | None = None
    upsell_salespage_url: str | None = None
    thankyou_url: str | None = None
    image_url: str | None = None
    product_type_id: ProductType | None = ProductType.DOWNLOADS
    currency: str | None = None
    approval_status: ApprovalStatus = ApprovalStatus.NEW
    affiliate_commission: float | None = None
    buyer_type: BuyerType = BuyerType.CONSUMER
    is_address_input_mandatory: DigiBool = DigiBool.FALSE
    add_order_data_to_thankyou_page_url: DigiBool = DigiBool.FALSE


@dataclasses.dataclass(kw_only=True)
class Product:
    id: parsable_to_int
    image_url: str
    user_id: parsable_to_int
    units_left: str
    owner_name: str
    owner_id: parsable_to_int
    is_quantity_editable_before_purchase: DigiBool
    is_quantity_editable_after_purchase: DigiBool
    thankyou_url: str
    affiliate_commission: parsable_to_float
    affiliate_commission_fix: parsable_to_float
    affiliate_commission_cur: str # currency
    is_address_input_mandatory: DigiBool
    is_phone_no_input_shown: DigiBool
    is_title_input_shown: DigiBool
    is_name_shown_on_bank_statement: DigiBool
    is_affiliation_auto_accepted: DigiBool
    name: str
    name_intern: str
    note: str
    tag: str
    language: str
    created_at: str
    modified_at: str
    product_group_id: int | None
    is_active: DigiBool
    currency: str
    description: str
    salespage_url: str
    upsell_salespage_url: str
    buyer_type: str # enum (business|consumer..)
    is_addon_thankyou_url_enabled: typing.Optional[DigiBool]
    has_addr_salutation: DigiBool
    image_id: str
    upsell_thankyou_page_url: str
    add_order_data_to_thankyou_page_url: DigiBool
    add_order_data_to_upsell_sales_page_url: str
    redirect_to_custom_upsell_thankyou_page: DigiBool
    add_order_data_to_upsell_thankyou_page_url: DigiBool
    product_type_id: parsable_to_int
    stop_sales_at: str
    encrypt_order_data_of_thankyou_page_url: str
    encrypt_order_data_of_upsell_thankyou_page_url: str
    is_vat_shown: DigiBool
    is_free_upsell_enabled: DigiBool
    is_free_upsell_started: DigiBool
    is_free_upsell_stopped: DigiBool
    upsell_freeflow_thankyou_url: str
    is_upsell_double_purchase_prevented: DigiBool
    is_optin_checkbox_shown: DigiBool
    optin_text: str
    country: str
    max_quantity: parsable_to_int
    description_thankyou_page: str
    orderform_id: parsable_to_int
    is_phone_no_mandatory: DigiBool
    is_search_engine_allowed: DigiBool
    pay_methods: str # enum (creditcard,paypal,banktransfer,ELV,test,sofortue)
    notify_payment_emails: str
    notify_refund_emails: str
    notify_chargeback_emails: str
    notify_missed_payment_emails: str
    notify_rebilling_start_stop_emails: str
    notify_rebilling_payment_emails: str
    notify_addons_for: str
    is_deleted: DigiBool
    approval_status: str
    approval_status_msg: str
    product_group_name: str = None
