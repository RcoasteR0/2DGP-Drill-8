from sdl2 import SDLK_SPACE


def space_down(e):
    return e[0] == 'INPUT' and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'



# 상태 머신을 관리해주는 클래스
class StateMachine:
    def __init__(self, o):
        self.o = o # boy self가 전달, self.o 상태머신과 연결된 캐릭터 객체
        self.event_que = [] # 발생하는 이벤트를 담는
        pass

    def update(self):  # Idle.do()
        self.cur_state.do(self.o)
        # 이벤트 발생했는지 확인하고, 거기에 따라서 상태변화를 수행
        if self.event_que:  # list 에 요소가 있으면, list 값은 True
            e = self.event_que.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e): # e가 지금 check_event 이면? space_down(e) ?
                    self.cur_state.exit(self.o)
                    self.cur_state = next_state
                    self.cur_state.enter(self.o)

    def start(self, start_state):
        # 현재 상태를 시작 상태로 만듬
        self.cur_state = start_state # Idle
        pass

    def draw(self):
        self.cur_state.draw(self.o)
        pass

    def set_transitions(self, transitions):
        self.transitions = transitions
        pass

    def handle_event(self, event):
        #event : input event
        #state machine event : (이벤트종류, 값)
        self.state_machine.add_event(
            'INPUT', event
        )

    def add_event(self, e):
        self.event_que.append(e)
