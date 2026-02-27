from whimbox.task.task_template import *
from whimbox.interaction.interaction_core import itt
from whimbox.common.utils.ui_utils import*
from whimbox.ui.ui_assets import *

class DeliveryBottleTask(TaskTemplate):
    def __init__(self, session_id):
        super().__init__(session_id=session_id, name="delivery_bottle_task")
    
    @register_step("投递漂流瓶")
    def step1(self):
        if not wait_until_appear(TextDeliveryBottle):
            self.update_task_result(status=STATE_TYPE_ERROR, message="未找到投递按钮")
            return STEP_NAME_FINISH
        itt.key_press(keybind.KEYBIND_INTERACTION)
        itt.wait_until_stable(threshold=0.95)
        if not scroll_find_click(AreaDialog, "确认投递", str_match_mode=0, need_scroll=False):
            self.update_task_result(status=STATE_TYPE_FAILED, message="未找到确认投递按钮")
            return STEP_NAME_FINISH
        itt.wait_until_stable(threshold=0.95)
        if not scroll_find_click(AreaDialog, "确认", str_match_mode=0, need_scroll=False):
            self.update_task_result(status=STATE_TYPE_FAILED, message="未找到确认按钮")
            return STEP_NAME_FINISH

    def handle_finally(self):
        pass

if __name__ == "__main__":
    task = DeliveryBottleTask(session_id="debug")
    print(task.task_run())

