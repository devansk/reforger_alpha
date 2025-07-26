import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utilities')))
from log_system import log

#gracz = Player() #tworzenie instacji klasy Player
#lista_enemy = Monsters() #tworzenie obiektu klasy Monsters
#enemy = lista_enemy.get_monster_by_id(1) #enemy przyjmuje Monster o id 1 -> krolik

class Fight:
    def __init__(self,player,enemy):
        self.player = player
        self.enemy = enemy
        
    
    def walka(self):
        enemy = self.enemy
        player = self.player
        hits = 0

        while player.is_alive and enemy.is_alive:
            hits += 1
            p_dmg = player.get_damage() #Pobranie obrażeń gracza
            p_dmg -= enemy.get_defense()

            enemy.reduce_hp(p_dmg) #Cios gracza
            log.log(f"{player.get_name()} hit {enemy.get_name()} for {p_dmg} damage", 1)
            if enemy.is_alive == False:  #Sprawdzenie czy przeciwnik umarł
                log.log(f"{enemy.get_name()} get killed by {player.get_name()} in {hits} hit(s)",2)

                player.add_experience(enemy.get_xp())
                log.log(f"{player.get_name()} get +{enemy.get_xp()}xp | [{player.get_experience()}/{player.get_experience_need()}]")

                drop_list = enemy.drop_item()
                for id in drop_list:
                    log.log(f"Item drops from {enemy.get_name()}",2)
                    player.add_inventory(id,'drop') 
                break

            player.reduce_health(enemy.get_attack()) #Cios przeciwnika
            log.log(f"{enemy.get_name()} hit {player.get_name()} for {enemy.get_attack()} damage", 2)
            if player.is_alive == False: #Sprawdzenie czy gracz umarł
                log.log(f"{player.get_name()} get killed by {enemy.get_name()} in {hits} hit(s)",1)
                player.set_experience(0)
                log.log(f"{self.get_name()} died and lost all exp",1)
                break
                


        

