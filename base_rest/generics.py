"""
Author: Sanidhya Mangal, Ravinder Singh
github:sanidhyamangal
email: sanidhya.mangal@engineerbabu
"""
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import GenericAPIView

from base import mixins


class BaseGenericAPIView(mixins.GetQuerySetMixin, GenericAPIView):
    """
    Generic class for API view ops
    """

    model_class = None
    serializer_class = None
    instance_name = None
    filter_backends = [SearchFilter, OrderingFilter]


class BaseAPIListCreate(BaseGenericAPIView, mixins.BaseAPIViewListMixin,
                        mixins.BaseAPIViewCreateMixin):
    """
    List and Create API view.
    """

    pass


class BaseAPIViewList(BaseGenericAPIView, mixins.BaseAPIViewListMixin):
    """
    Base API View Class for performing list op
    """

    pass


class BaseAPIViewCreate(mixins.BaseAPIViewCreateMixin, BaseGenericAPIView):
    """
    Base API View Class for performing create op
    """

    pass


class BaseAPIViewDetails(BaseGenericAPIView, mixins.ReterieveAPIViewMixin,
                         mixins.UpdateAPIViewMixin,
                         mixins.DestroyAPIViewMixin):
    """
    Base Class for performing details api view
    """

    pass


class BaseAPIViewReterieve(BaseGenericAPIView, mixins.ReterieveAPIViewMixin):
    """
    Base Class for performing reterieve api view
    """

    pass


class BaseAPIViewUpdate(BaseGenericAPIView, mixins.UpdateAPIViewMixin,
                        mixins.ReterieveAPIViewMixin):
    """
    Base Class for performing view and update api view
    """

    pass


class BaseAPIViewDelete(BaseGenericAPIView, mixins.ReterieveAPIViewMixin,
                        mixins.DestroyAPIViewMixin):
    """
    Base Class for performing delete and view api
    """

    pass


class BaseAPIUpdateDelete(BaseGenericAPIView, mixins.UpdateAPIViewMixin,
                          mixins.DestroyAPIViewMixin):
    """
    Base Class for performing update and delete api
    """

    pass
