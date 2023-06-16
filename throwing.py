import Interface

class Throwing:
    def __init__(self) -> None:
        pass

    @staticmethod
    def direction(cor_x:float, cor_y:float, area: float):
        if 0 <= cor_x <0.47:
            print('turn left')
        elif 0.53 <= cor_x <=1:
            print('turn right')
        elif 0.47 <= cor_x < 0.53:
            print('go forward or throw ball')
            if area >= 0.25:
                print('throw ball')
                return False
            else:
                print('Go forward')
        return True

         
    