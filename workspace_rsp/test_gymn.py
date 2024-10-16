import buzzer
import rgb_panel
import config as cfg

rgb_panel = rgb_panel.RGBPanel()
rgb_panel.set_all([cfg.WHITE, cfg.WHITE, cfg.BLUE, cfg.BLUE, cfg.BLUE, cfg.RED, cfg.RED, cfg.RED])
buzzer = buzzer.Buzzer()
buzzer.play_music(0, buzzer.melody_russian_gymn, buzzer.beet_russian_gymn)
rgb_panel.turn_off()
