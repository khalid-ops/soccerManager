from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .models import UserRegistry, Teams, PlayersRegistry
import os
from datetime import datetime
import json
import traceback
from soccer_fantasy.players_file import PlayerManager
# Create your views here.

pm = PlayerManager()
market_account_id = 9
market_team_players_id = 6

@api_view(['POST'])
def user_registration(request):

    try:
        user_data = request.data
        team_generated = False
        players_added = False
        if user_data is not None:  
            user_email = user_data['email']
            if UserRegistry.objects.filter(user_email=user_email).exists():
                response_payload = {'status' : "User already exists"}
                return Response(response_payload, status=200)
            
            UserRegistry.objects.create(
                user_name=user_data['name'],
                user_email=user_data['email'],
                user_password=user_data['password'],
                phone_number=user_data['phone'],
                status=False
            )
            if UserRegistry.objects.filter(user_email=user_email).exists():
                new_user = UserRegistry.objects.get(user_email=user_email).id

                team_generated = pm.generate_team(new_user)
                if team_generated:
                    players_added = pm.generate_players(new_user)

            if team_generated and players_added:

                response_payload = {'status' : "Account created successfully!"}
                return Response(response_payload, status=200)
            else:
                response_payload = {'status' : "Account creation failed! Try again :("}
                return Response(response_payload, 200)
        else:
            response_payload = {'status': "Invalid Data"}
            return Response(response_payload, status=200)
    except:
        return Response({'status' : 'system error'}, 500)

@api_view(['POST'])
def user_login(request):

    try:
        login_info = request.data
        user_email = login_info['userEmail']
        if login_info is not None:
            if UserRegistry.objects.filter(user_email=user_email).exists():
                user_data = UserRegistry.objects.get(user_email=user_email)
                user_pass = user_data.user_password
                if user_pass == login_info['userPassword']:
                    UserRegistry.objects.filter(user_email=user_email).update(status=True)
                    data = UserRegistry.objects.get(user_email=user_email)
                    user_data_list = {
                    'id' : data.id,
                    'name' : data.user_name,
                    'email' : data.user_email,
                    'accountStatus' : data.status
                    }
                    response_payload = {
                        'status' : "Login Successful",
                        'userData' : user_data_list
                        }
                    return Response(response_payload, status=200)
                else:
                    response_payload = {
                        'status' : "Login Failed",
                        }
                    return Response(response_payload, 200)
            else:
                response_payload = {
                    'status' : "User doesn't exist!"
                }
                return Response(response_payload, 200)
        else:    
            response_payload = {
                'status' : "Invalid credentials! Try again"
            }
            return Response(response_payload, 200)
    except:
        return Response({'status' : 'system error'}, 500)

@api_view(['GET'])
def user_logout(request):

    try:
        user_id = request.query_params['userId']
        if UserRegistry.objects.filter(id=user_id).exists():
            UserRegistry.objects.filter(id=user_id).update(status=False)
            response_payload = {
            'status' : "Logged out Successfully"
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                'status' : "Invalid request!"
            }
            return Response(response_payload,200)
    except:
        return Response({'status' : 'system error'}, 500)
    

@api_view(['GET'])
def get_users_teams_details(request):
    try:
        user_id = request.query_params['userId']
        if user_id is not None:
            if Teams.objects.filter(owned_by=user_id).exists():
                teams_data = Teams.objects.filter(owned_by=user_id)
                teams_data_item = teams_data[0]
                current_team_id = teams_data_item.id
                teams_data = json.loads(serializers.serialize('json', teams_data))
                players_data = PlayersRegistry.objects.filter(player_team=current_team_id)
                players_data = json.loads(serializers.serialize('json', players_data))

                teams_data_list = {
                    'id' : teams_data[0]['pk'],
                    'teams_details' : teams_data[0]['fields'],
                }
                players_data_list = []
                for player in players_data:
                    data = {
                        'id' : player['pk'],
                        'player_details' : player['fields']
                    }
                    players_data_list.append(data)

                response_payload = {
                    'status' : "success",
                    'teams_data' : teams_data_list,
                    'players_data' : players_data_list
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'status' : 'User doesnt own a team!'
                }
                return Response(response_payload, 200)
        else:
            response_payload = {
                'status' : 'Invalid userid'
            }
            return Response(response_payload, 200)
    except:
        return Response({'status' : 'system error'}, 500)
    
@api_view(['POST'])
def update_teams_data(request):
    try:
        user_id = request.data['userId']
        updation_data = request.data['teamData']
        if Teams.objects.filter(owned_by=user_id).exists():
            Teams.objects.filter(owned_by=user_id).update(
                team_name=updation_data['teamName'],
                team_country=updation_data['teamCountry'],
                updated_at = datetime.utcnow(),
                )
            response_payload = {
                'status' : 'Updated successfully'
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                'status' : 'Team not found'
            }
            return Response(response_payload, 200)
    except:
        response_payload = {
            'status' : 'system error'
            }
        return Response(response_payload, 500)

@api_view(['POST'])    
def update_players_data(request):
    try:
        user_id = request.data['userId']
        player_id = request.data['playerId']
        new_player_first_name = request.data['playerFirstName']
        new_player_last_name = request.data['playerLastName']
        new_player_country = request.data['playerCountry']
        if Teams.objects.filter(owned_by=user_id).exists():
            if PlayersRegistry.objects.filter(id=player_id).exists():
                PlayersRegistry.objects.filter(id=player_id).update(
                    player_firstname=new_player_first_name,
                    player_lastname=new_player_last_name,
                    player_country=new_player_country,
                )
                response_payload = {
                    'status' : 'Updated successfully'
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'status' : 'Player Not found'
                }
                return Response(response_payload, 200)
        else:
            response_payload = {
                    'status' : 'Invalid request'
                }
            return Response(response_payload, 200)
    except:
        return Response({'status' : 'system error'}, 500)

@api_view(['POST'])
def transfer_players(request):

    try:
        user_id = request.data['userId']
        transfer_data = request.data['transferData']
        if UserRegistry.objects.filter(id=user_id).exists():
            result = pm.transfer_playersto_market(user_id, transfer_data)
            if result:
                response_payload = {
                    'status' : "success"
                }
                return Response(response_payload, 200)
            else:
                response_payload = {
                    'status' : "Team or player doesnt exist"
                }
                return Response(response_payload, 200)
        else:
            response_payload = {
                'status' : "User not found"
            }
            return Response(response_payload, 200)
    except:
        return Response({'status' : 'system error'}, 500)
    
@api_view(['GET'])
def get_market_players(request):

    try:
        user_id = request.query_params['userId']
        players_data = PlayersRegistry.objects.filter(player_team=market_team_players_id)
        if players_data is not None:
            players_data = json.loads(serializers.serialize('json', players_data))

            market_players_list = []
            for player in players_data:
                data = {
                    'id' : player['pk'],
                    'players_details' : player['fields']
                }
                market_players_list.append(data)

            response_payload = {
                'status' : 'success',
                'playersData' : market_players_list
            }
            return Response(response_payload, 200)
        else:
            response_payload = {
                'status' : 'no players found'
            }
            return Response(response_payload, 200)
    except:
        return Response({'status' : 'system error'}, 500)
    
@api_view(['POST'])
def to_buy_player(request):
    try:
        user_id = request.data['userId']
        player_id = request.data['playerId']
        if UserRegistry.objects.filter(id=user_id).exists():
            result, message = pm.buy_players(user_id, player_id)

            if result:
                response_payload = {
                    'status' : message
                }
                return Response(response_payload, 200) 
            else:
                response_payload = {
                    'status' : message,
                }
                return Response(response_payload, 200)
        else:
            response_payload = {
                'status' : 'user not found'
            }
            return Response(response_payload, 200)

    except:
        return Response({'status' : 'system error'}, 500)