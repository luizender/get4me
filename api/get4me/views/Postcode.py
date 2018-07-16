from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from get4me.serializers import PostcodeSerializer
from get4me.models import GuardiansModel
from .postcode import PostCodeInformation, GMapsDistance

class PostcodeView(viewsets.ReadOnlyModelViewSet):

    queryset = GuardiansModel.objects.all()
    serializer_class = PostcodeSerializer

    def _build_full_address(self):
        self.address = self.request.GET.get('address', None)
        self.district = self.request.GET.get('district', None)
        self.city = self.request.GET.get('city', None)
        self.state = self.request.GET.get('state', None)
        self.postcode = self.request.GET.get('postcode', None)
        self.country = self.request.GET.get('country', None)

        if self.postcode and not self.address or not self.district or not self.city or not self.state:
            pcInfo = PostCodeInformation(self.postcode)
            pcInfo.consult()

            self.address = pcInfo.get_address()
            self.district = pcInfo.get_district()
            self.city = pcInfo.get_city()
            self.state = pcInfo.get_state()

        if self.district and self.city and self.state:
            full_address = '%s%s%s%s%s%s' % (
                self.address + ',' if self.address else '',
                self.district + ',' if self.district else '',
                self.city + ',' if self.city else '',
                self.state + ',' if self.state else '',
                self.postcode + ',' if self.postcode else '',
                self.country if self.country else ''
            )

            if full_address[-1:] == ',':
                return full_address[:-1]

        return None

    def get_queryset(self):
        return GuardiansModel.objects.filter_by_info(
            self.state, self.city, self.district
        )

    def list(self, request, *args, **kwargs):
        full_address = self._build_full_address()
        if not full_address:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        gmaps = GMapsDistance(full_address)
        for guardian in queryset:
            gmaps.add_destination(guardian.id, guardian.full_address())
        gmaps_data = gmaps.get_distance_duration()

        serializer = self.get_serializer(queryset, gmaps_data=gmaps_data, many=True)

        return Response(serializer.data)