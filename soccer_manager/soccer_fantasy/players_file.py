from django.shortcuts import render
from django.core import serializers
from .models import UserRegistry, Teams, PlayersRegistry
from datetime import datetime
import random
import os
import json
import traceback

class PlayerManager:
    def __init__(self):
        self.player_types_counts = {
            'goalkeepers'  : 3,
            'defenders'  : 6,
            'midfielders'  : 6,
            'attackers' : 5
        }
        self.total_players = 20
        self.marketaccountteam = 6
        self.team_value = 5000000
        self.player_value = 1000000
        self.countries = ['India', 'USA', 'UK', 'Canada', 'China']

    def generate_team(self, user_id):
        try:
            if UserRegistry.objects.filter(id=user_id).exists():
                user_data = UserRegistry.objects.get(id=user_id)
                default_team_name = user_data.user_name+"s team"
                random_num = random.randint(0,4)
                default_country_name = self.countries[random_num]
                default_team_value = (self.total_players * self.player_value) + self.team_value
                Teams.objects.create(
                    team_name = default_team_name,
                    team_country = default_country_name,
                    team_value = default_team_value,
                    owned_by = UserRegistry.objects.get(id=user_id),
                    created_at = datetime.utcnow(),
                    updated_at = datetime.utcnow()
                )
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False
        
    def generate_players(self, user_id):

        try:
            if Teams.objects.filter(owned_by=user_id).exists():
                team_data = Teams.objects.get(owned_by=user_id)
                team = team_data.team_name
                for p in self.player_types_counts:
                    player_type = p
                    count = self.player_types_counts[p]
                    for i in range(count):
                        player_country = random.randint(0, 4)
                        print(player_country)
                        player_age = random.randint(18, 41)
                        player_first_name = player_type+str(i+1)
                        player_last_name = "byuser"+team
                        PlayersRegistry.objects.create(
                            player_firstname = player_first_name,
                            player_lastname = player_last_name,
                            player_age = player_age,
                            player_country = self.countries[player_country],
                            player_team = Teams.objects.get(team_name=team),
                            player_value = self.player_value
                        )
                return True
            else:
                return False
        except:
            traceback.print_exc()

    def buy_players(self, user_id, player_id):
        try:
            print(user_id, player_id)
            random_factor = random.randint(10, 100)
            if Teams.objects.filter(owned_by=user_id).exists():
                team_data = Teams.objects.filter(owned_by=user_id)
                team_data = team_data[0]
                current_team_id = team_data.id
                current_team_budget = team_data.team_budget
                current_team_value = team_data.team_value
                players_data = PlayersRegistry.objects.filter(id=player_id)
                players_data = json.loads(serializers.serialize('json', players_data))
                players_data = players_data[0]['fields']
                previous_team_id = players_data['player_team']
                increased_player_value = ((players_data['player_value']*random_factor)/100) + players_data['player_value']
                if current_team_budget >= players_data['player_value']:
                    current_team_budget = current_team_budget - players_data['player_value']
                    current_team_value = current_team_value + increased_player_value
                    Teams.objects.filter(owned_by=user_id).update(
                        team_budget = current_team_budget,
                        team_value = current_team_value
                    )
                    PlayersRegistry.objects.filter(id=player_id).update(
                        player_team = current_team_id,
                        player_value = increased_player_value
                    )
                    if previous_team_id != self.marketaccountteam:
                        prev_team = Teams.objects.filter(id=previous_team_id)
                        prev_team = json.loads(serializers.serialize('json', prev_team))
                        prev_team = prev_team[0]['fields']
                        prev_team_value = prev_team['team_value']
                        prev_team_value += players_data['player_value']
                        Teams.objects.filter(id=previous_team_id).update(
                            team_value = prev_team_value
                        )
                    return True, "success"
                else:
                    return False, "Insufficient budget"
            else:
                return False, "Team Not found"

        except:
            traceback.print_exc()

    def transfer_playersto_market(self, user_id, player_data):
        try:
            player_id = player_data['playerId']
            new_player_value = player_data['playerNewValue']
            print(player_id, new_player_value)
            if Teams.objects.filter(owned_by = user_id).exists():
                team = Teams.objects.get(owned_by = user_id)
                if PlayersRegistry.objects.filter(id=player_id).exists():
                    player = PlayersRegistry.objects.filter(id=player_id)
                    player = json.loads(serializers.serialize('json',player))
                    player_data_value = player[0]['fields']
                    current_player_value = player_data_value['player_value']
                    if team.id == player_data_value['player_team']:
                        PlayersRegistry.objects.filter(id=player_id).update(
                            player_value = new_player_value,
                            player_team = self.marketaccountteam
                        )
                        new_team_value = team.team_value - current_player_value
                        Teams.objects.filter(id=team.id).update(
                            team_value = new_team_value
                        )
                        return True
                else:
                    return False
            else:
                return False
        except:
            traceback.print_exc()