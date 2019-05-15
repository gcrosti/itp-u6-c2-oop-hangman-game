from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self,guess,hit=None,miss=None):
        self.guess = guess
        self.hit = hit
        self.miss = miss
        if hit and miss:
            raise InvalidGuessAttempt()
    
    def is_hit(self):
        if self.hit:
            return True
        return False
        
    def is_miss(self):
        if self.miss:                
            return True
        return False
    

class GuessWord(object):
    def __init__(self,answer):
        self.answer = answer
        self.masked = '*'*len(self.answer)
        if not answer:
            raise InvalidWordException()
        
    def perform_attempt(self,guess):
        if len(guess)>1:
            raise InvalidGuessedLetterException()
        attempt = GuessAttempt(guess)
        if guess.lower() in self.answer.lower():
            attempt.hit = True
            masked_list = list(self.masked)
            for i in range(len(self.answer)):
                if self.answer[i].lower() == guess.lower():
                    masked_list[i] = guess.lower()
            self.masked = ''.join(masked_list)
        else:
            attempt.miss = True
        return attempt
        

class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self,word_list=None,number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))
     
    @classmethod    
    def select_random_word(cls,l_words):
        if not l_words:
            raise InvalidListOfWordsException()
        return random.choice(l_words)

    
    def guess(self,guess):
        if self.is_finished():
            raise GameFinishedException()
        if self.is_won():
            raise GameWonException()
        if self.is_lost():
                raise GameLostException()
        attempt = self.word.perform_attempt(guess)
        self.previous_guesses.append(guess.lower())
        if self.is_won():
            raise GameWonException()
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException()
        return attempt
    
    def is_won(self):
        if self.word.masked==self.word.answer:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses==0:
            return True
        return False
       
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
