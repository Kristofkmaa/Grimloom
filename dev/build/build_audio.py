import subprocess, base64, json, os
A='/home/claude/itch/audio/'; O='/home/claude/grimloom/build/aud/'
SFX={
 'hit':'rpg/10_Battle_SFX/15_Impact_flesh_02.wav', 'crit':'rpg/10_Battle_SFX/22_Slash_04.wav', 'kill':'rpg/10_Battle_SFX/69_Enemy_death_01.wav',
 'hurt':'rpg/12_Player_Movement_SFX/61_Hit_03.wav', 'block':'rpg/10_Battle_SFX/39_Block_03.wav', 'miss':'rpg/10_Battle_SFX/35_Miss_Evade_02.wav',
 'forge':'kenney/OGG/metalPot1.ogg', 'forge2':'kenney/OGG/metalPot2.ogg', 'coins':'kenney/OGG/handleCoins.ogg',
 'door':'kenney/OGG/doorOpen_1.ogg', 'creak':'kenney/OGG/creak1.ogg', 'page':'kenney/OGG/bookFlip1.ogg',
 'encounter':'rpg/10_Battle_SFX/55_Encounter_02.wav', 'slam':'rpg/8_Atk_Magic_SFX/30_Earth_02.wav',
 'level':'rpg/8_Buffs_Heals_SFX/30_Revive_03.wav', 'reward':'rpg/10_UI_Menu_SFX/013_Confirm_03.wav', 'equip':'rpg/10_UI_Menu_SFX/070_Equip_10.wav',
 'unequip':'rpg/10_UI_Menu_SFX/071_Unequip_01.wav', 'sell':'rpg/10_UI_Menu_SFX/079_Buy_sell_01.wav', 'denied':'rpg/10_UI_Menu_SFX/033_Denied_03.wav',
 'fire':'rpg/8_Atk_Magic_SFX/04_Fire_explosion_04_medium.wav', 'ice':'rpg/8_Atk_Magic_SFX/13_Ice_explosion_01.wav', 'thunder':'rpg/8_Atk_Magic_SFX/18_Thunder_02.wav',
 'poison':'rpg/8_Atk_Magic_SFX/46_Poison_01.wav', 'charge':'rpg/8_Atk_Magic_SFX/45_Charge_05.wav', 'buff':'rpg/8_Buffs_Heals_SFX/16_Atk_buff_04.wav',
 'shield':'rpg/8_Buffs_Heals_SFX/17_Def_buff_01.wav', 'speed':'rpg/8_Buffs_Heals_SFX/48_Speed_up_02.wav', 'heal':'rpg/8_Buffs_Heals_SFX/02_Heal_02.wav',
 'claw':'rpg/10_Battle_SFX/03_Claw_03.wav', 'bite':'rpg/10_Battle_SFX/08_Bite_04.wav',
}
MUS={'explore':'music/Free Dark Fantasy Music/WAV/Elkmire Keep (LOOP).wav','boss':'music/Free Dark Fantasy Music/WAV/Library of Veles (LOOP).wav'}
out={'sfx':{},'music':{}}; tot=0
def enc(src,dst,br,trim):
    af=['silenceremove=start_periods=1:start_threshold=-50dB'] if trim else []
    cmd=['ffmpeg','-y','-v','error','-i',A+src,'-ac','1','-ar','44100']+(['-af',','.join(af)] if af else [])+['-b:a',br,dst]
    subprocess.run(cmd,check=True); return open(dst,'rb').read()
for k,v in SFX.items():
    b=enc(v,O+k+'.mp3','48k',True); out['sfx'][k]='data:audio/mpeg;base64,'+base64.b64encode(b).decode(); tot+=len(b)
for k,v in MUS.items():
    b=enc(v,O+k+'.mp3','56k',False); out['music'][k]='data:audio/mpeg;base64,'+base64.b64encode(b).decode(); tot+=len(b); print(k,len(b)//1024,'KB')
open('/home/claude/grimloom/assets_audio.js','w').write('ASSETS.audio = '+json.dumps(out)+';\n')
print('total',tot//1024,'KB')
