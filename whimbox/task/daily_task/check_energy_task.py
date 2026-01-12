from whimbox.task.task_template import *
from whimbox.ui.ui import ui_control
from whimbox.ui.page_assets import *
from whimbox.interaction.interaction_core import itt

class CheckEnergyTask(TaskTemplate):
    def __init__(self, need_cost_energy=0):
        super().__init__("check_energy_task")
        self.need_cost_energy = need_cost_energy

    @register_step("检查体力")
    def step1(self):
        ui_control.goto_page(page_daily_task)
        energy_text = itt.ocr_single_line(AreaZxxyEnergy)
        try:
            energy = int(energy_text.split("/")[0])
            self.log_to_gui(f"剩余体力：{energy}, 需要消耗体力：{self.need_cost_energy}")
            if energy < self.need_cost_energy + 10:
                self.update_task_result(status=STATE_TYPE_FAILED, message=f"剩余体力有可能不足")
            else:
                self.update_task_result(message=f"剩余体力充足")
        except:
            self.update_task_result(status=STATE_TYPE_FAILED, message=f"体力识别异常:{energy_text}")