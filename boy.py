from pico2d import load_image, get_time

from state_machine import StateMachine, space_down, time_out, right_down, left_down, left_up, right_up, start_event, \
    a_down


class Idle:
    @staticmethod
    def enter(boy, e):
        if left_up(e) or right_down(e):
            boy.action = 2
            boy.face_dir = -1
        elif right_up(e) or left_down(e) or start_event(e):
            boy.action = 3
            boy.face_dir = 1

        boy.frame = 0
        boy.dir = 0

        # 시작 시간을 기록
        boy.start_time = get_time()
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 2:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass

class Sleep:
    @staticmethod
    def enter(boy, e):
        pass
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        pass
    @staticmethod
    def draw(boy):
        if boy.face_dir == 1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 300, 100, 100,
                3.141592 / 2,  # 회전 각도
                '',  # 좌우상하 반전 X
                boy.x - 25, boy.y - 25, 100, 100
            )
        elif boy.face_dir == -1:
            boy.image.clip_composite_draw(
                boy.frame * 100, 200, 100, 100,
                -3.141592 / 2,  # 회전 각도
                '',  # 좌우상하 반전 X
                boy.x + 25, boy.y - 25, 100, 100
            )
        pass

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0
    @staticmethod
    def exit(boy, e):
        pass
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        if boy.x < 10:
            boy.x = 10
        elif boy.x > 790:
            boy.x = 790
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class AutoRun:
    @staticmethod
    def enter(boy, e):
        boy.dir = boy.face_dir
        if boy.face_dir == 1:
            boy.action = 1
        elif boy.face_dir == -1:
            boy.action = 0

        boy.start_time = get_time()
    @staticmethod
    def exit(boy, e):
        boy.face_dir = boy.dir
        if boy.face_dir == 1:
            boy.action = 3
        elif boy.face_dir == -1:
            boy.action = 2
    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 10
        if boy.x < 20:
            boy.x = 20
            boy.dir = 1
            boy.action = 1
        elif boy.x > 780:
            boy.x = 780
            boy.dir = -1
            boy.action = 0

        if get_time() - boy.start_time > 2:
            boy.state_machine.add_event(('TIME_OUT', 0))
        pass
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            0, '',
            boy.x, boy.y + 40, 200, 200
        )



class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체를 위한 상태 머신인지 알려줄 필요
        self.state_machine.start(Idle) # 객체를 생성한게 아니고 직접 Idle 클래스를 사용
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, a_down: AutoRun, time_out: Sleep},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
                AutoRun: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event : input event
        # state machine event : (이벤트종류, 값)
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
