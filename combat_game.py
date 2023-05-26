import random
import sys

class Player:
    def __init__(self, role, name):
        self.health = 50
        self.max_health = 50 
        self.defense = 0
        self.mana = 100
        self.max_mana = 100 
        self.role = role
        self.name = name
        self.healthpotion_count = 1

        if self.role == "tank":
            self.health = 75
            self.max_health = 75
            self.mana = 50
            self.max_mana = 50
            self.defense = 2

    def damage_done(self):
        return random.randint(1,20)

    def damage_taken(self, cost):
        self.health -= abs(cost)

    def mana_gained(self, cost):
        self.mana += abs(cost)

    def mana_spent(self, cost):
        self.mana -= cost

    def healing_done(self):
        return random.randint(1,20)

    def healing_received(self, cost):
        self.health += abs(cost)

    def cast_basic_spell(self, spell_name, y):
        self.mana_spent(10)
        return self.result_damage_done(spell_name, self.calc_damage(spell_name, y))

    def cast_powerful_spell(self, spell_name, y):
        self.mana_spent(25)
        return self.result_damage_done(spell_name, 1.5 * self.calc_damage(spell_name, y))

    def cast_basic_heal(self, spell_name, y):
        self.mana_spent(20)
        return self.result_healing_done(spell_name, self.calc_healing(spell_name), y)

    def cast_powerful_heal(self, spell_name, y):
        self.mana_spent(35)
        return self.result_healing_done(spell_name, 1.5 * self.calc_healing(spell_name), y)

    def cast_evocation(self):
        self.mana_gained(self.max_mana)
        print(f"{self.name} casts Evocation")
        print(f"{self.name} has refilled their mana to {self.max_mana} mana!")

    def use_healthpotion(self):
        self.healing_received(20)
        self.healthpotion_count -= 1
        damage_done = 0
        print(f"{self.name} uses a Healthpotion!")
        print(f"{self.name} gains 20 health")
        return damage_done

    def crit_miss_chance(self, spell, y, damage_done):
        crit = random.randint(1,20)
        if enemy_party[y].role == "tank":
            if crit <= 3:
                damage_done = damage_done*0
                print(f"{spell} was parried by the opposing tank!")
        else:
            if crit == 20:
                damage_done = damage_done * 2
                print(f"{spell} critically hit!")
            elif crit == 1:
                damage_done = damage_done*0
                print(f"{spell} misses!")
            else:
                damage_done = damage_done
        return damage_done

    def crit_heal(self, spell, healing_done):
        critheal = random.randint(1,20)
        if critheal == 20:
            healing_done = healing_done * 2
            print(f"{spell} critically hit!")
        else:
            healing_done = healing_done
        return healing_done

    def calc_damage(self, spell_name, y):             
        return self.crit_miss_chance(spell_name, y, self.damage_done())

    def calc_healing(self, spell_name):
        return self.crit_heal(spell_name, self.healing_done())

    def result_damage_done(self, spell_name, damage_done):
        print(f"{self.name} casts {spell_name}")
        print(f"{self.name} deals {damage_done} damage")
        return damage_done

    def result_healing_done(self, spell_name, healing_done, y):      
        print(f"{self.name} cast {spell_name}")
        print(f"{self.name} heals {attacking_party[y].name} for {healing_done} health")
        return healing_done

    def choose_action(self):
        if self.role == "tank":
            return self.choose_action_tank()
        elif self.role == "dps":
            return self.choose_action_dps()
        elif self.role == "healer":
            return self.choose_action_healer()
        else:
            print("There seems to have been a typo, try running the program again")

    def choose_action_dps(self):
        action = input("Basic Spell, Powerful Spell, Evocation, or Healthpotion?:  ").lower()
        if action == "basic spell" or action == "powerful spell":
            return self.action_attack(action)
        else:
            self.action_evo_healthpotion(action)

    def choose_action_healer(self):
        action = input("Attack, Basic Heal, Powerful Heal, Evocation, or Healthpotion?:  ").lower()
        if action == "attack":
            return self.action_attack(action)
        elif action == "evocation" or action == "healthpotion":
            self.action_evo_healthpotion(action)
        else:
            return self.action_heal(action)

    def choose_action_tank(self):
        damage_done = 0
        action = input("Attack, Evocation, or Healthpotion?:  ").lower()
        if action == "attack":
            return self.action_attack(action)            
        elif action == "evocation" or action == "healthpotion":
            self.action_evo_healthpotion(action)
        return damage_done

    def action_attack(self, action):
        damage_done = 0
        while True:
            target = input(f"Are you targeting {enemy_party[0].name} or {enemy_party[1].name}?: ").lower()
            y = self.set_target(target, "harm")
            if y != -1:
                break
            print("Invalid target. Please select a valid target.")
        
        if action == "attack" or action == "basic spell":
            if self.mana >= 10:
                damage_done = self.cast_basic_spell(input("Name of Spell: "), y)
                enemy_party[y].damage_taken(damage_done)
            else:
                print(f"That spell costs 10 mana and you have {self.mana} mana!")
                self.choose_action()
        else:
            if self.mana >= 25:
                damage_done = self.cast_powerful_spell(input("Name of Spell: "), y)
                enemy_party[y].damage_taken(damage_done)
            else:
                print(f"That spell costs 25 mana and you have {self.mana} mana!")
                self.choose_action()
        if enemy_party[y].health <= 0:
            print(f"{enemy_party[y].name} has been knocked down!")
        if enemy_party[y].role == "tank":
            damage_done -= enemy_party[y].defense
            if damage_done < 0:
                damage_done = 0
        return damage_done

    def action_heal(self, action):
        healing_done = 0
        while True:
            target = input(f"Are you targeting {attacking_party[0].name} or {attacking_party[1].name}?: ").lower()
            y = self.set_target(target, "help")
            if y != -1:
                break
            print("Invalid target. Please select a valid target.")
        if action == "basic heal":
            if self.mana >= 20:
                healing_done = self.cast_basic_heal(input("Name of Spell: "), y)
                attacking_party[y].healing_received(healing_done)
            else:
                print(f"That spell costs 10 mana and you have {self.mana} mana!")
                self.choose_action_healer()
        elif action == "powerful heal":
            if self.mana >= 35:
                healing_done = self.cast_powerful_heal(input("Name of Spell: "), y)
                attacking_party[y].healing_received(healing_done)
            else:
                print(f"That spell costs 10 mana and you have {self.mana} mana!")
                self.choose_action_healer()
        return healing_done

    def action_evo_healthpotion(self, action):
        if action == "evocation":
            self.cast_evocation()
        else:
            if self.healthpotion_count > 0:
                self.use_healthpotion()
            else:
                print("You don't have any healthpotions!")
                self.choose_action()

    def set_target(self, target, intent):
        if intent == "help":
            target_party=attacking_party
        elif intent == "harm":
            target_party=enemy_party
        else:
            print("There seems to have been an error in setting up the action in question. Please end the program.")
            sys.exit()
        for i, player in enumerate(target_party):
            if target == player.name:
                return i
        return -1  # Invalid target, indicating the target wasn't found


    def update_resources(self):
        if self.mana < self.max_mana:
            if self.mana+5>self.max_mana:
                self.mana=self.max_mana
            else:
                self.mana += 5
            print(f"{self.name} regenerates 5 mana")
        else:
            self.mana = self.max_mana
        if self.health > self.max_health:
            self.health = self.max_health

# Function to validate role input
def validate_role_input(role):
    return role.lower() in ['dps', 'tank', 'healer']

# Get Stats
def create_player(name):
    name = name.lower()
    role = ''
    while not validate_role_input(role):
        role = input(f"{name}, enter DPS, Tank, or Healer: ").lower()
    return Player(role, name)

player1 = create_player(input("Name of Player 1: "))
player2 = create_player(input("Name of Player 2: "))
player3 = create_player(input("Name of Player 3: "))
player4 = create_player(input("Name of Player 4: "))

#list putting players into teams
party1 = [player1, player2]
party2 = [player3, player4]

#selecting which team goes first
attacking_party = random.choice([party1, party2])
if attacking_party == party1:
    enemy_party = party2
else:
    enemy_party = party1

game_status = True
count = 1           #tracks what round it is, has no interactions currently
print("\n")        #puts a gap of space after name/role selection
#taking turns attacking
while game_status:
    for i in range(0,2):
        if attacking_party[i].health <= 0:
            print("You are too injured to fight right now D:")  #can be healed back over 0 hp allowing attacks again
        else:
            print(f"it is {attacking_party[i].name}'s Turn. They have {attacking_party[i].mana} mana and {attacking_party[i].health} health remaining")
            attacking_party[i].choose_action()
            attacking_party[i].update_resources() #adjusts in the event hp/mana is over 100 (not perfect- could be improved. But it does allow for strategy involving not attacking the overhealed player effectively wasting a heal)
        count += .25
        print("\n")
#check for win condition
    if enemy_party[0].health <= 0 and enemy_party[1].health <= 0:   #as it stands, the teams round must end, could be improved to auto-end when both are down
        print(f"Congratulations {attacking_party[0].name} and {attacking_party[1].name} you win!")
        game_status = False
    else:
        attacking_party, enemy_party = enemy_party, attacking_party
