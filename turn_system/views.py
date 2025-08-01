from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.place.models import Place
from apps.custom_user.authentication_mixin import IsAdminRole
from apps.custom_user.models import CustomUser
from apps.turn.models import Turn
from apps.turn.views import avg_attendacy_time
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class StatsAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def get(self, request,pk=None):
        if pk is not None:
            try:
                place = Place.objects.get(pk=pk)
            except Place.DoesNotExist:
              return Response({"error": "Lugar no encontrado"}, status=404)
            data = []
            place_data = []

            h_priority_attended = 0
            m_priority_attended = 0
            l_priority_attended = 0
            disability_attended = 0
            older_adults_attended = 0
            normal_attended = CustomUser.objects.filter(priority='L', owned_turns__active=False, owned_turns__canceled=False).distinct().count()
            total_attended_users_count = CustomUser.objects.filter(owned_turns__active=False, owned_turns__canceled=False).distinct().count()

            place_turns = Turn.objects.filter(place_id=pk)
            non_canceled_attended_turns = place_turns.filter(
                active=False, canceled=False)
            canceled_turns = place_turns.filter(
                active=False, canceled=True)
            active_turns = place_turns.filter(
                place_id=place, active=True)

            older_adults_attended += non_canceled_attended_turns.filter(
                owner__age__gte=60).count()
            disability_attended += non_canceled_attended_turns.filter(
                owner__condition=True).count()
            h_priority_attended += non_canceled_attended_turns.filter(
                owner__priority="H").count()
            m_priority_attended += non_canceled_attended_turns.filter(
                owner__priority="M").count()
            l_priority_attended += non_canceled_attended_turns.filter(
                owner__priority="L").count()


            if non_canceled_attended_turns.exists():
                avg_time = round(avg_attendacy_time(
                    non_canceled_attended_turns), 2)
            else:
                avg_time = "Desconocido"

            active_place_turn_count = active_turns.count()
            attended_place_turn_count = non_canceled_attended_turns.count()
            canceled_place_turn_count = canceled_turns.count()
            total_place_turn_count = place_turns.count()

            place_data.append({
                'place_name': place.place_name,
                'total_place_turn_count': total_place_turn_count,
                'active_turn_count': active_place_turn_count,
                'attended_turn_count': attended_place_turn_count,
                'canceled_turn_count': canceled_place_turn_count,
                'avg_attendancy_time': avg_time
            })
            if total_attended_users_count:
                older_adults_attended_percentage = older_adults_attended / \
                                                   total_attended_users_count * 100
                discapacity_attended_percentage = older_adults_attended / \
                                                  total_attended_users_count * 100
                normal_attended_percentage = normal_attended / total_attended_users_count * 100
            else:
                older_adults_attended_percentage = 0
                discapacity_attended_percentage = 0
                normal_attended_percentage = 0

            data.append({
                'attended_users_demographic_distribution': {
                    'total_attended': total_attended_users_count,
                    'older_adults_attended': older_adults_attended,
                    'older_adults_percentage': older_adults_attended_percentage,
                    'discapacity_attended': disability_attended,
                    'discapacity_attended_percentage': discapacity_attended_percentage,
                    'normal_attended': normal_attended,
                    'normal_attended_percentage': normal_attended_percentage
                },
                'attended_users_priority_distribution': {
                    'h_priority_attended': h_priority_attended,
                    'm_priority_attended': m_priority_attended,
                    'l_priority_attended': l_priority_attended
                },
                'place_statistics': place_data
            })

            return Response(data, status=status.HTTP_200_OK)

        else:
            places = Place.objects.all()

            data = []
            place_data = []

            h_priority_attended = 0
            m_priority_attended = 0
            l_priority_attended = 0
            disability_attended = 0
            older_adults_attended = 0

            normal_attended = CustomUser.objects.filter(priority='L', owned_turns__active=False, owned_turns__canceled=False).distinct().count()
            total_attended_users_count = CustomUser.objects.filter(owned_turns__active=False, owned_turns__canceled=False).distinct().count()

            for place in places:
                place_turns = Turn.objects.filter(place_id=place)
                non_canceled_attended_turns = place_turns.filter(
                    active=False, canceled=False)
                canceled_turns = place_turns.filter(
                    active=False, canceled=True)
                active_turns = place_turns.filter(
                    place_id=place, active=True)

                older_adults_attended += non_canceled_attended_turns.filter(
                    owner__age__gte=60).count()
                disability_attended += non_canceled_attended_turns.filter(
                    owner__condition=True).count()
                h_priority_attended += non_canceled_attended_turns.filter(
                    owner__priority="H").count()
                m_priority_attended += non_canceled_attended_turns.filter(
                    owner__priority="M").count()
                l_priority_attended += non_canceled_attended_turns.filter(
                    owner__priority="L").count()

                if non_canceled_attended_turns.exists():
                    avg_time = round(avg_attendacy_time(
                        non_canceled_attended_turns), 2)
                else:
                    avg_time = "Desconocido"

                active_place_turn_count = active_turns.count()
                attended_place_turn_count = non_canceled_attended_turns.count()
                canceled_place_turn_count = canceled_turns.count()
                total_place_turn_count = place_turns.count()

                place_data.append({
                    'place_name': place.place_name,
                    'total_place_turn_count': total_place_turn_count,
                    'active_turn_count': active_place_turn_count,
                    'attended_turn_count': attended_place_turn_count,
                    'canceled_turn_count': canceled_place_turn_count,
                    'avg_attendancy_time': avg_time
                })

            if total_attended_users_count:
                older_adults_attended_percentage = older_adults_attended / \
                    total_attended_users_count * 100
                discapacity_attended_percentage = older_adults_attended / \
                    total_attended_users_count * 100
                normal_attended_percentage = normal_attended / total_attended_users_count * 100
            else:
                older_adults_attended_percentage = 0
                discapacity_attended_percentage = 0
                normal_attended_percentage = 0

            data.append({
                'attended_users_demographic_distribution': {
                    'total_attended': total_attended_users_count,
                    'older_adults_attended': older_adults_attended,
                    'older_adults_percentage': older_adults_attended_percentage,
                    'discapacity_attended': disability_attended,
                    'discapacity_attended_percentage': discapacity_attended_percentage,
                    'normal_attended': normal_attended,
                    'normal_attended_percentage': normal_attended_percentage
                },
                'attended_users_priority_distribution': {
                    'h_priority_attended': h_priority_attended,
                    'm_priority_attended': m_priority_attended,
                    'l_priority_attended': l_priority_attended
                },
                'place_statistics': place_data
            })

            return Response(data, status=status.HTTP_200_OK)

