import rw_na, rw_eu, rw_eu2, rw_as, rw_af, rw_af2, rw_la, rw_la2
M = {"P":"political","W":"war","E":"economic","I":"ideas","R":"religion","S":"science","C":"culture"}
REWRITE = {}
for rid, parts in [("na",[rw_na.R]),("eu",[rw_eu.R,rw_eu2.R]),("as",[rw_as.R]),("af",[rw_af.R,rw_af2.R]),("la",[rw_la.R,rw_la2.R])]:
    for part in parts:
        for head,(cats,w,hook,story,then,now) in part.items():
            REWRITE[rid+"|"+head] = ([M[c] for c in cats], w, hook, story, then, now)

TOP = {
# North America
"First enslaved Africans arrive in Virginia","Declaration of Independence","Constitution written","Civil War begins","Emancipation Proclamation",
"Wright brothers fly","Stock market crash","Pearl Harbor → US enters WWII","Atomic bombs; UN founded","Marshall Plan","Cuban Missile Crisis",
"Moon landing","Civil Rights Act","9/11 attacks","Financial crisis; Obama elected","COVID-19 pandemic",
# Europe
"Gutenberg's printing press","Ottomans take Constantinople","Luther's 95 Theses","Newton's Principia","Peace of Westphalia","Watt's steam engine",
"Adam Smith's Wealth of Nations","French Revolution","Waterloo; Congress of Vienna","Britain abolishes slavery","Revolutions of 1848; Communist Manifesto",
"Darwin's Origin of Species","WWI begins","Russian Revolution","Treaty of Versailles","Hitler takes power","WWII begins","Germany invades USSR",
"Germany surrenders; Holocaust revealed","NATO founded; Germany divided","Treaty of Rome (EEC)","Berlin Wall falls","USSR dissolves; Yugoslav wars begin","Russia invades Ukraine",
# Asia & Middle East
"Vasco da Gama reaches India","Battle of Plassey","First Opium War","Meiji Restoration","Japan defeats Russia","Qing dynasty falls","Sykes-Picot Agreement",
"Hiroshima & Nagasaki","India & Pakistan partition","Israel founded","People's Republic of China","Deng's market reforms",
"Iranian Revolution; USSR invades Afghanistan","China joins WTO; US invades Afghanistan",
# Africa
"Portuguese begin Atlantic slave trade","Suez Canal opens","Berlin Conference: Scramble for Africa","Ethiopia defeats Italy at Adwa","Apartheid begins",
"Ghana independent","'Year of Africa'","Rwandan genocide; Mandela president",
# Latin America
"Columbus reaches the Caribbean","Tenochtitlan falls","Potosí silver discovered","Haitian Revolution begins","Panama Canal opens","Cuban Revolution",
}
for k,v in list(REWRITE.items()):
    head = k.split("|",1)[1]
    REWRITE[k] = (v[0], 3 if head in TOP else min(v[1],2)) + v[2:]
