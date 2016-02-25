class attacker(object):
 
   def __init__(self):
        self._attackerID = 1
        
   def __init__(self):
        self._ip_address = 1
    
   	@property
    def attackerID(self):
        return self._attackerID
        
    @property
    def ip_address(self):
        return self._ip_address
        
        @attackerID.setter
    def attackerID(self, value):
        self._attackerID = value
        
        @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value
        
        
        
    --------------------------------------
    
    class victim(object):
 
   def __init__(self):
        self._victimID = 1
        
   def __init__(self):
        self._ip_address = 1
        
	def __init__(self):
        self._name = 1
        
   def __init__(self):
        self._role = 1
    
   @property
    def victimID(self):
        return self._victimID
        
    @property
    def ip_address(self):
        return self._ip_address
        
    @property
    def name(self):
        return self._name
        
    @property
    def role(self):
        return self._role
        
        @victimID.setter
    def victimID(self, value):
        self._victimID = value
        
        @ip_address.setter
    def ip_address(self, value):
        self._ip_address = value
        
        @name.setter
    def name(self, value):
        self._name = value
        
        @role.setter
    def role(self, value):
        self._role = value
        
        --------------------------------------------
        
class attack(object):
 
   def __init__(self):
        self._attackID = 1
        
   def __init__(self):
        self._source_port = 1
        
	def __init__(self):
        self._attackerID = 1
        
   def __init__(self):
        self._destination_port = 1
        
        def __init__(self):
        self._victimID = 1
        
   def __init__(self):
        self._attack_name = 1
        
        def __init__(self):
        self._protocol = 1
        
   def __init__(self):
        self._level = 1
        
    def __init__(self):
        self._attack_date = 1
        
   @property
    def attackID(self):
        return self._attackID
        
    @property
    def source_port(self):
        return self._source_port
        
    @property
    def attackerID(self):
        return self._attackerID
        
    @property
    def destination_port(self):
        return self._destination_port

 	@property
    def victimID(self):
        return self._victimID
        
    @property
    def attack_name(self):
        return self._attack_name
        
    @property
    def protocol(self):
        return self._protocol
        
    @property
    def level(self):
        return self._level
        
     @property
    def attack_date(self):
        return self._attack_date
        
                
        @attackID.setter
    def attackID(self, value):
        self._attackID = value
        
        @source_port.setter
    def source_port(self, value):
        self._source_port = value
        
         @attackerID.setter
    def attackerID(self, value):
        self._attackerID = value
        
        @destination_port.setter
    def destination_port(self, value):
        self._destination_port = value
        
         @victimID.setter
    def victimID(self, value):
        self._victimID = value
        
        @attack_name.setter
    def attack_name(self, value):
        self._attack_name = value
        
         @protocol.setter
    def protocol(self, value):
        self._protocol = value
        
        @level.setter
    def level(self, value):
        self._level = value
        
         @attack_date.setter
    def attack_date(self, value):
        self._attack_date = value
        
    --------------------------------------
    
class attack_persistence(object):
 
   def __init__(self):
        self._attackpersistenceID = 1
        
   def __init__(self):
        self._attackID = 1
        
	def __init__(self):
        self._persistence_count = 1
        
   def __init__(self):
        self._response = 1
    
   		@property
    def attackpersistenceID(self):
        return self._attackpersistenceID
        
    	@property
    def attackID(self):
        return self._attackID
        
    	@property
    def persistence_count(self):
        return self._persistence_count
        
       @property
    def response(self):
        return self._response
        
        @attackpersistenceID.setter
    def attackpersistenceID(self, value):
        self._attackpersistenceID = value
        
        @attackID.setter
    def attackID(self, value):
        self._attackID = value
        
        @persistence_count.setter
    def persistence_count(self, value):
        self._persistence_count = value
        
        @response.setter
    def response(self, value):
        self._response = value
        
        ----------------------------------------------
        
class response(object):
 
   def __init__(self):
        self._responseID = 1
        
   def __init__(self):
        self._response_time = 1
        
    def __init__(self):
        self._attackID = 1
    
   	@property
    def responseID(self):
        return self._responseID
        
    @property
    def response_time(self):
        return self._response_time
        
    @property
    def attackID(self):
        return self._attackID
        
        @responseID.setter
    def responseID(self, value):
        self._responseID = value
        
        @response_time.setter
    def response_time(self, value):
        self._response_time = value
        
        @attackID.setter
    def attackID(self, value):
        self._attackID = value
        
        
        ------------------------------------------
 
 class TCP_Reset(object):
 
   def __init__(self):
        self._tcp_resetID = 1
        
   def __init__(self):
        self._responseID = 1
    
   @property
    def tcp_resetID(self):
        return self._tcp_resetID
        
    @property
    def responseID(self):
        return self._responseID
        
        @tcp_resetID.setter
    def tcp_resetID(self, value):
        self._tcp_resetID = value
        
        @responseID.setter
    def responseID(self, value):
        self._responseID = value
        
        ----------------------------------------
        
class Timebased_Block(object):
 
   def __init__(self):
        self._timebased_blockID = 1
        
   def __init__(self):
        self._responseID = 1
        
    def __init__(self):
        self._time_blocked = 1
    
   	@property
    def timebased_blockID(self):
        return self._timebased_blockID
        
    @property
    def responseID(self):
        return self._responseID
        
    @property
    def time_blocked(self):
        return self._time_blocked
        
        @timebased_blockID.setter
    def timebased_blockID(self, value):
        self._timebased_blockID = value
        
        @responseID.setter
    def responseID(self, value):
        self._responseID = value
        
        @time_blocked.setter
    def time_blocked(self, value):
        self._time_blocked = value
        
        -------------------------------------------
        
class Permanent_Block(object):
 
   def __init__(self):
        self._permanent_blockID = 1
        
   def __init__(self):
        self._responseID = 1
    
   @property
    def permanent_blockID(self):
        return self._permanent_blockID
        
    @property
    def responseID(self):
        return self._responseID
        
        @permanent_blockID.setter
    def permanent_blockID(self, value):
        self._permanent_blockID = value
        
        @responseID.setter
    def responseID(self, value):
        self._responseID = value
        
