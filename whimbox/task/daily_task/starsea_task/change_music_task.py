from whimbox.task.task_template import *
from whimbox.interaction.interaction_core import itt
from whimbox.common.utils.ui_utils import*
from whimbox.ui.ui_assets import *

class ChangeMusicTask(TaskTemplate):
    def __init__(self, session_id):
        super().__init__(session_id=session_id, name="change_music_task")
    
    @register_step("更改音乐")
    def step1(self):
        if not wait_until_appear(TextChangeMusic):
            self.update_task_result(status=STATE_TYPE_FAILED, message="未找到更改音乐按钮")
            return STEP_NAME_FINISH
        itt.key_press(keybind.KEYBIND_INTERACTION)
        itt.delay(1, comment="等待进入留声机页面")
        back_to_page_main()
