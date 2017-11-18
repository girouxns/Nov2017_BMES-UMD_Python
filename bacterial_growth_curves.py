#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Nick Giroux
@collaborators: Sonya Williams, Manaahil Rao
@hours_spent: 5
"""

import random
import matplotlib.pyplot as plt

class Bacteria(object):
    """ Simplified representation of bacteria (does not model drug effects) """
    def __init__(self, max_reproduction_prob, clear_prob):
        """
        Initializes a Bacteria instance, saving the data attributes of the instance.

        :param float reproduction_prob: Probability of reproducing during a time step (0-1)
        :param float clear_prob: Probability of being cleared from the body during a time step (0-1)
        """
        self.max_reproduction_prob = float(max_reproduction_prob)
        self.clear_prob = float(clear_prob)

    def does_clear(self):
        """ 
        Stochastically determines whether this bacterial cell is cleared from the body. 
        Uses self.clear_prob to interpret result from random.random(). 

        :return: Whether this cell is cleared from the body
        :rtype: bool
        """
        bool_cleared = False
        check = random.random()
        if check < self.clear_prob:
            bool_cleared = True
        elif check > self.clear_prob:
            bool_cleared = False
        return bool_cleared

    def reproduce(self, population_density):
        """ 
        Stochastically determines whether this bacterial cell reproduces at a given time step, and
        if so returns a new instance of same time. If it does not reproduce, returns None. 

        The probability of reproduction is defined as:
        self.max_reproduction_prob * (1 - population_density)
        The idea is that if there is no population pressure, the bacteria reproduces with
        self.max_reproduction_prob, however as the bacterial population grows towards its
        maximum sustainable population, the growth rate will be inhibited as 1 - population density
        (population density is defined as population / maximum sustainable population)

        :param float population_density: Bacterial population as a fraction of total sustainable population
        :return: A new Bacteria instance if it reproduces, otherwise None
        :rtype: Bacteria or None
        """
        check = random.random()
        bool_reproduced = False
        prob_reproduction = self.max_reproduction_prob * (1 - population_density)
        if check < prob_reproduction:
            bool_reproduced = True
        elif check > prob_reproduction:
            bool_reproduced = False
        if bool_reproduced:
            return Bacteria(self.max_reproduction_prob, self.clear_prob)
        else:
            return None

class Patient(object):
    """
    Represents a simplified patient's body.
    """
    def __init__(self, bacteria, max_population):
        """
        Initializes a Patient
        :param list bacteria: A list of Bacteria objects
        :param int max_population: The maximum sustainable bacterial population in the patient's body
        """
        self.bacteria = list(bacteria)
        self.max_population = int(max_population)

    def get_pop(self):
        """ Returns the size of the current bacterial population (an integer) """
        return int(len(self.bacteria))

    def get_bacteria(self):
        """ Returns the list of bacteria infecting the patient """
        return list(self.bacteria)

    def update(self):
        """
        Updates the state of the baceterial population by a single time step. 

        Performs the following steps, in this order:
        1. Determines whether each bacterial cell survives, and updates a list of survivors accordingly
        2. Computes the current population density
        3. Determines whether each bacterial cell reproduces, and if so adds it to the list of
        bacteria in the patient. 

        Hint: it's easiest to operate with separate lists for steps 1 and 3, and then reconcile these lists
        with self.bacteria AFTER you've finished operating on the separate lists (in the case of 1, that
        would mean replacing the data attribute list at the end of the step with the temporary list, while 
        in 3, you would want to update the data attribute list using entries from the temporary list). 
        
        :return: Nothing
        :rtype: None
        """
        # Remove dead bacteria
        surviving_bacteria, dead_bacteria = [], []
        for bacterium in list(self.bacteria):
            bool_die = bool(bacterium.does_clear())
            if bool_die:
                dead_bacteria.append(bacterium)
            elif not bool_die:
                surviving_bacteria.append(bacterium)
        
        # Get population density
        population_density = len(surviving_bacteria)/self.max_population
        
        # Add children
        children = []
        for bacterium in list(surviving_bacteria):
            potential_child = bacterium.reproduce(population_density)
            if potential_child:
                children.append(potential_child)
        
        updated_bacteria = surviving_bacteria + children
        self.bacteria = updated_bacteria

        return None

def simple_simulation(num_bacteria, max_pop, max_reproduction_prob, clear_prob, trials, time_steps=300):
    """
    Runs a simulation and generates a plot of the average bacterial population in the patient as a function
    of number of time steps. 

    For each of `trials` trials, this function instantiates a Patient, runs a simulation for `time_steps`
    timesteps, and then plots the average Bacterial population size as a function of time. 

    :param int num_bacteria: Initial number of Bacteria infecting the Patient
    :param int max_pop: Maximum population of Bacteria that can live in the Patient
    :param float max_reproduction_prob: Maximum reproduction probability (float from 0-1)
    :param float clear_prob: Probability of a Bacteria dying at any one timestep
    :param int trials: Number of simulations to execute (and average the results of)
    :return: Returns nothing
    :rtype: None
    """
    patient_bacteria = []
    for i in range(num_bacteria):
        patient_bacteria.append(Bacteria(max_reproduction_prob, clear_prob))
    
    patient_trials = []
    avg_pop_at_t, sum_pop_at_t = [], 0
    for j in range(trials):
        patient = Patient(patient_bacteria, max_pop)
        patient_trials.append(patient)
        sum_pop_at_t += patient.get_pop()
    avg_pop_at_t.append(sum_pop_at_t/trials)
    
    for t in range(time_steps-1):
        sum_pop_at_t = 0
        for single_patient in patient_trials:
            single_patient.update()
            sum_pop_at_t += single_patient.get_pop()
        avg_pop_at_t.append(sum_pop_at_t/trials)
        
    f,ax = plt.subplots()
    ax.plot(range(time_steps), avg_pop_at_t)
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of bacterial cells in the patient')
    ax.set_title('Simple Patient simulation, params:' + str(num_bacteria) + '|' + str(max_pop) + '|' + str(max_reproduction_prob) + '|' + str(clear_prob) + '|' + str(trials))
    ax.legend(['Bacterial Population'])
    plt.show()

    return None

simple_simulation(200, 1000, .15, .1, 100)

class DrugResistantBacteria(Bacteria):
    """ Bacterial representation that models drug resistance """
    def __init__(self, max_reproduction_prob, clear_prob, is_resistant, mutation_probability):
        """
        Initializes a DrugResistantBacteria instance, saving the parameters of the instance.
        Subclasses Bacteria and uses Bacteria's __init__ to handle max_reproduction_prob and 
        clear_prob.

        :param float reproduction_prob: Probability of reproducing during a time step (0-1)
        :param float clear_prob: Probability of being cleared from the body during a time step (0-1)
        :param bool is_resistant: Whether or not this bacterial cell is resistant to an antibiotic
        :param float mutation_probability: Probability of cell's antibiotic resistance mutating (from not resistant to
        resistant, as well as from resistant to not resistant)
        """
        self.max_reproduction_prob = max_reproduction_prob
        self.clear_prob = clear_prob
        self.is_resistant = is_resistant
        self.mutation_probability = mutation_probability

    def reproduce(self, population_density, antibiotic_being_administered):
        """ 
        Stochastically determines whether this bacterial cell reproduces at a given time step, and
        if so returns a new instance of same time. If it does not reproduce, returns None. 
        Child cell has same antibiotic resistance as parent with probability 1 - mutation_probability
        (child antibiotic resistance mutates with likelihood of mutation_probability, otherwise stays
        the same) 

        The probability of reproduction is defined as:
        self.max_reproduction_prob * (1 - population_density)
        The idea is that if there is no population pressure, the bacteria reproduces with
        self.max_reproduction_prob, however as the bacterial population grows towards its
        maximum sustainable population, the growth rate will be inhibited as 1 - population density
        (population density is defined as population / maximum sustainable population)

        If the antibiotic is being administered, non-resistant bacteria are unable to reproduce during
        the time step. Resistant bacteria reproduce as normal. 

        :param float population_density: Bacterial population as a fraction of total sustainable population
        :param bool antibiotic_being_administered: Whether or not the antibiotic is being administered
        :return: A new DrugResistantBacteria instance if it reproduces, otherwise None
        :rtype: DrugResistantBacteria or None
        """
        check_reproduced = random.random()
        check_mutation = random.random()
        
        new_resistance = self.is_resistant
        prob_reproduction = self.max_reproduction_prob * (1 - population_density)
        
        if antibiotic_being_administered:   # if the antibiotic is administered
            if not self.is_resistant or check_reproduced > prob_reproduction: # and the bacteria is not resistant
                return None # no reproduction
            elif self.is_resistant and check_reproduced < prob_reproduction:  # and the bacteria is resistant, check probability
                if check_mutation < self.mutation_probability:  # check probability for mutation
                    new_resistance = not self.is_resistant
                return DrugResistantBacteria(self.max_reproduction_prob, self.clear_prob, new_resistance, self.mutation_probability) # returns a new instance
        
        elif not antibiotic_being_administered and check_reproduced < prob_reproduction: # if no antibiotic is administered
            if check_mutation < self.mutation_probability:  # don't check if resistant, just probability of mutation
                new_resistance = not self.is_resistant
            return DrugResistantBacteria(self.max_reproduction_prob, self.clear_prob, new_resistance, self.mutation_probability) # returns a new instance
        
        elif check_reproduced > prob_reproduction:
            return None
        

    def get_resistance(self):
        """ Returns True if Bacteria is antibiotic resistant, otherwise False """
        return bool(self.is_resistant)

class TreatedPatient(Patient):
    """
    Represents a patient's body which is being treated with antibiotics.
    """
    def __init__(self, bacteria, max_population, antibiotic_being_administered):
        """
        Initializes a TreatedPatient. Subclasses Patient and uses Patient's __init__
        internally for bacteria and max_population.

        :param list bacteria: A list of Bacteria objects
        :param int max_population: The maximum sustainable bacterial population in the patient's body
        :param bool antibiotic_being_administered: Whether or not the antibiotic is being administered
        """
        self.bacteria = bacteria
        self.max_population = max_population
        self.antibiotic_being_administered = antibiotic_being_administered

    def add_prescription(self):
        """
        Administer an antibiotic to this patient. After a prescription is added,
        the drug acts on the bacterial population for all subsequent time steps. 
        If the antibiotic is already being prescribed, this method has no effect.
        """
        self.antibiotic_being_administered = True

    def get_resistant_pop(self):
        """ Returns the size of the current antibiotic-resistant bacterial population (an integer) """
        counter = 0
        for bacterium in self.bacteria:
            if bacterium.get_resistance():
                counter += 1
        return counter

    def update(self):
        """
        Updates the state of the baceterial population by a single time step. 

        Performs the following steps, in this order:
        1. Determines whether each bacterial cell survives, and updates the list accordingly
        2. Determines the current population density
        3. Determines whether each bacterial cell reproduces, and if so add it to the list of
            bacteria in the patient. 
        
        :return: Nothing
        :rtype: None
        """
        # Remove dead bacteria
        surviving_bacteria, dead_bacteria = [], []
        for bacterium in list(self.bacteria):
            bool_die = bool(bacterium.does_clear())
            if bool_die:
                dead_bacteria.append(bacterium)
            elif not bool_die:
                surviving_bacteria.append(bacterium)
        
        # Get population density
        population_density = len(surviving_bacteria)/self.max_population
        
        # Add children
        children = []
        for bacterium in list(surviving_bacteria):
            potential_child = bacterium.reproduce(population_density, self.antibiotic_being_administered)
            if potential_child:
                children.append(potential_child)
        
        updated_bacteria = surviving_bacteria + children
        self.bacteria = updated_bacteria

        return None

def simulation_with_antibiotic(num_bacteria, max_pop, max_reproduction_prob, clear_prob, trials, mutation_probability, time_steps=300):
    """
    Runs a simulation and generates a plot of the average bacterial population in the patient as a function
    of number of time steps. 

    For each of `trials` trials, this function instantiates a TreatedPatient, runs a simulation for `time_steps`
    timesteps, and then plots the average Bacterial population size as a function of time. 

    This simulations assumes that an antibiotic is prescribed at time step 150 (and acts on the 
    DrugResistantBacteria population for all subsequent timesteps). 

    :param int num_bacteria: Initial number of Bacteria infecting the Patient
    :param int max_pop: Maximum population of Bacteria that can live in the Patient
    :param float max_reproduction_prob: Maximum reproduction probability (float from 0-1)
    :param float clear_prob: Probability of a Bacteria dying at any one timestep
    :param int trials: Number of simulations to execute (and average the results of)
    :return: Returns nothing
    :rtype: None
    """
    patient_bacteria = []
    for i in range(num_bacteria):
        patient_bacteria.append(DrugResistantBacteria(max_reproduction_prob, clear_prob, False, mutation_probability))
    
    patient_trials = []
    avg_pop_at_t, sum_pop_at_t = [], 0
    avg_resistant_pop_at_t, sum_resistant_pop_at_t = [], 0
    for j in range(trials):
        patient = TreatedPatient(patient_bacteria, max_pop, False)
        patient_trials.append(patient)
        sum_pop_at_t += patient.get_pop()
        sum_resistant_pop_at_t += patient.get_resistant_pop()
    avg_pop_at_t.append(sum_pop_at_t/trials)
    avg_resistant_pop_at_t.append(sum_resistant_pop_at_t/trials)
    
    for t in range(time_steps-1):
        sum_pop_at_t = 0
        sum_resistant_pop_at_t = 0
        for single_patient in patient_trials:
            if t == 150:
                single_patient.add_prescription()
            single_patient.update()
            sum_pop_at_t += single_patient.get_pop()
            sum_resistant_pop_at_t += single_patient.get_resistant_pop()
        avg_pop_at_t.append(sum_pop_at_t/trials)
        avg_resistant_pop_at_t.append(sum_resistant_pop_at_t/trials)
        
    f,ax = plt.subplots()
    ax.plot(range(time_steps), avg_pop_at_t)
    ax.plot(range(time_steps), avg_resistant_pop_at_t)
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of bacterial cells in the patient')
    ax.set_title('Simple Patient simulation, params:' + str(num_bacteria) + '|' + str(max_pop) + '|' + str(max_reproduction_prob) + '|' + str(clear_prob) + '|' + str(trials) + '|' + str(mutation_probability))
    ax.legend(['Bacterial Population', 'Resistant'])
    plt.show()

    return None

simulation_with_antibiotic(100, 1000, .1, .05, 100, .005)
