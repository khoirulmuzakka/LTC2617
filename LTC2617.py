"""Author : Khoirul Faiq Muzaka"""
import smbus
import time

#command register 
write_to_input = 0b0000
power_up_DAC = 0b0001
write_and_powerup = 0b0011
power_down = 0b0100
no_operation = 0b1111

#Output Channel
address_DAC_A = 0b0000
address_DAC_B = 0b0001
address_all_DACs = 0b1111

V_REF = 5.0
V_REFLO = 0

bus = smbus.SMBus(1)


class LTC2617(object) :
    """Basic functionality of DAC"""
    
    def __init__(self, address = 0x41):
        self.address = address
        self.__power_up()  
                   
            
    def __pointer_register(self, command_register, DAC_A , DAC_B ):
        def DAC_channel_address():
            try :
                assert DAC_A in [0,1] and DAC_B in [0,1]
                if DAC_A == 1:
                    if DAC_B == 0:
                        return 0b0000
                    else :
                        return 0b1111
                else :
                    if DAC_B ==1 :
                        return 0b0001
                    else :
                        raise ValueError 
            except AssertionError :
                print ("The value of argument must be 0 or 1")
            except ValueError :
                print ("can not be both zero")
                
        return (command_register << 4) | DAC_channel_address()      
    
    
    def write (self, V_out, DAC_A = 1, DAC_B = 1) :
        """Write V_out volts to DAC"""
        try :
            assert abs(V_out) <= V_REF
            data = (int(((V_out-V_REFLO)/(V_REF-V_REFLO))*2**14) << 2) & 0xFFFF
            bus.write_i2c_block_data(self.address, self.__pointer_register(write_and_powerup, DAC_A , DAC_B), [(data >> 8) & 0xFF, data & 0xFF])
            time.sleep(0.1)            
        except AssertionError :
            print ("The maxium value of V_out is V_REF")
        except IOError :
            print ("Device is not connected")             
        
    def __power_up (self, DAC_A =1, DAC_B =1):
        """Power up or update either or both DAC"""
        try :
            bus.write_i2c_block_data(self.address, self.__pointer_register(power_up_DAC, DAC_A, DAC_B), [0,0])
        except IOError :
            print ("Device is not connected or Address is wrong")
        
    def power_down (self, DAC_A =1, DAC_B=1):
        """Power down or update either or both DAC"""
        try :
            bus.write_i2c_block_data(self.address, self.__pointer_register( power_down, DAC_A, DAC_B), [0,0])
            
        except IOError:
            print ("Device is not connected")
            
    def test(self, V_out, DAC_A =1, DAC_B =0, minute = 1):
        timeout=time.time() + 60*minute
        while time.time() < timeout :
            try :
                self.write(V_out, DAC_A, DAC_B)
            except KeyboardInterrupt :
                break
            
            
            
            
        
        
    
     


