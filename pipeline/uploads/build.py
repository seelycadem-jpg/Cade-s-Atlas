from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

DECADES = list(range(1440, 2030, 10))
col = {d: i + 2 for i, d in enumerate(DECADES)}  # column B = 1440s

ERAS = [
    (1440, 1510, "RENAISSANCE", "C9A227"),
    (1520, 1640, "REFORMATION & WARS OF RELIGION", "8E6C3A"),
    (1650, 1770, "ABSOLUTISM & ENLIGHTENMENT", "5B7DB1"),
    (1780, 1840, "AGE OF REVOLUTIONS", "B0413E"),
    (1850, 1900, "INDUSTRIALIZATION & HIGH IMPERIALISM", "4F6D4A"),
    (1910, 1940, "WORLD WARS", "4A4A4A"),
    (1950, 1980, "COLD WAR & DECOLONIZATION", "2F5D7C"),
    (1990, 2020, "GLOBALIZATION & DIGITAL AGE", "6A4C93"),
]
EXPLORE = [
    (1440, 1590, "Age of Exploration — Portugal & Spain open sea routes; first global empires", "E8D9B0"),
    (1600, 1760, "Age of Mercantilism — chartered companies, colonies, Atlantic slave trade", "D9CBB4"),
    (1770, 1840, "Atlantic Revolutions — republics replace monarchies across the Americas & France", "EBC4BF"),
    (1850, 1900, "New Imperialism — Europe & Japan carve up Africa and Asia", "C8D5C3"),
    (1910, 1940, "Total War & Totalitarianism", "CFCFCF"),
    (1950, 1980, "Bipolar world — US vs USSR; ~100 new nations", "BFD0DC"),
    (1990, 2000, "Unipolar moment — US primacy, globalization, War on Terror", "D6CCE4"),
    (2010, 2020, "Return of great-power rivalry — China rises, Russia revisionist", "E4CCE0"),
]
CONFLICTS = [
    (1440, 1450, "End of Hundred Years' War (1453); Fall of Constantinople (1453)"),
    (1460, 1480, "Wars of the Roses (England)"),
    (1490, 1550, "Italian Wars; Ottoman expansion into Europe"),
    (1560, 1590, "French Wars of Religion; Dutch Revolt"),
    (1600, 1640, "Thirty Years' War"),
    (1650, 1710, "Anglo-Dutch Wars; Wars of Louis XIV"),
    (1720, 1740, "Colonial rivalry; peak Atlantic slave trade"),
    (1750, 1760, "Seven Years' War — first global war"),
    (1770, 1780, "American Revolution"),
    (1790, 1810, "French Revolution & Napoleonic Wars"),
    (1820, 1840, "Latin American independence; Concert of Europe"),
    (1850, 1860, "Wars of nationalism & unification (US Civil War, Italy, Germany)"),
    (1870, 1900, "Scramble for Africa; Opium Wars legacy"),
    (1910, 1910, "World War I"),
    (1920, 1930, "Depression; rise of fascism"),
    (1940, 1940, "World War II"),
    (1950, 1980, "Cold War: Korea, Vietnam, proxy wars"),
    (1990, 2000, "Gulf War, Balkans, 9/11 & War on Terror"),
    (2010, 2020, "Syria, Ukraine, Gaza"),
]
TECH = [
    (1440, 1490, "Printing press (c.1440) — ideas spread fast"),
    (1500, 1590, "Caravels, navigation, gunpowder empires"),
    (1600, 1680, "Scientific Revolution — telescope, Newton"),
    (1690, 1750, "Joint-stock companies, central banks"),
    (1760, 1830, "1st Industrial Revolution — steam & textiles"),
    (1840, 1860, "Railways & telegraph"),
    (1870, 1900, "2nd Industrial Revolution — steel, electricity, oil"),
    (1910, 1930, "Cars, aviation, radio"),
    (1940, 1960, "Nuclear weapons, jets, computers, space race"),
    (1970, 1980, "Microchip & personal computer"),
    (1990, 2000, "Internet"),
    (2010, 2020, "Smartphones & AI"),
]

REGIONS = {
"United States / North America": ("1F4E79", "DCE6F1", {
1490: ["1497 Cabot reaches Newfoundland"],
1530: ["1534 Cartier explores the St. Lawrence"],
1580: ["1587 Roanoke colony (later 'lost')"],
1600: ["1607 Jamestown founded", "1608 French found Quebec"],
1610: ["1619 First enslaved Africans arrive in Virginia; first elected assembly"],
1620: ["1620 Mayflower lands at Plymouth"],
1630: ["1630 Massachusetts Bay Colony"],
1660: ["1664 English seize New Amsterdam → New York"],
1670: ["1675 King Philip's War", "1676 Bacon's Rebellion"],
1680: ["1682 Penn founds Pennsylvania"],
1690: ["1692 Salem witch trials"],
1730: ["1739 Stono slave rebellion"],
1750: ["1754 French & Indian War begins"],
1760: ["1763 Britain wins Canada (Treaty of Paris)", "1765 Stamp Act"],
1770: ["1770 Boston Massacre", "1773 Boston Tea Party", "1775 Lexington & Concord", "1776 Declaration of Independence"],
1780: ["1781 Victory at Yorktown", "1783 Independence recognized", "1787 Constitution written"],
1790: ["1791 Bill of Rights", "1793 Cotton gin → slavery expands"],
1800: ["1803 Louisiana Purchase", "1804 Lewis & Clark", "1808 Atlantic slave imports banned"],
1810: ["1812 War of 1812", "1819 Florida acquired"],
1820: ["1820 Missouri Compromise", "1823 Monroe Doctrine", "1825 Erie Canal"],
1830: ["1830 Indian Removal Act", "1838 Trail of Tears"],
1840: ["1845 Texas annexed; 'Manifest Destiny'", "1846 Mexican-American War", "1848 Gold Rush; Seneca Falls"],
1850: ["1850 Compromise of 1850", "1854 Kansas-Nebraska Act", "1857 Dred Scott decision"],
1860: ["1861 Civil War begins", "1863 Emancipation Proclamation; Gettysburg", "1865 Union wins; Lincoln killed; 13th Amendment", "1867 Alaska purchased", "1869 Transcontinental railroad"],
1870: ["1876 Little Bighorn", "1877 Reconstruction ends → Jim Crow"],
1880: ["1882 Chinese Exclusion Act", "1886 Haymarket affair; AFL founded"],
1890: ["1890 Wounded Knee; frontier 'closed'", "1896 Plessy v. Ferguson", "1898 Spanish-American War; Hawaii annexed"],
1900: ["1901 T. Roosevelt; Progressive Era", "1903 Wright brothers fly", "1908 Model T"],
1910: ["1913 Federal Reserve; income tax", "1917 US enters WWI", "1919 Wilson's 14 Points; Senate rejects League"],
1920: ["1920 Women's suffrage (19th Am.)", "1929 Stock market crash"],
1930: ["1933 FDR's New Deal", "1935 Social Security"],
1940: ["1941 Pearl Harbor → US enters WWII", "1945 Atomic bombs; UN founded", "1947 Truman Doctrine", "1948 Marshall Plan"],
1950: ["1950 Korean War", "1954 Brown v. Board", "1955 Montgomery bus boycott", "1957 Sputnik shock"],
1960: ["1962 Cuban Missile Crisis", "1963 JFK assassinated", "1964 Civil Rights Act", "1965 Voting Rights Act; Vietnam escalation", "1968 MLK & RFK killed", "1969 Moon landing"],
1970: ["1971 Dollar leaves gold standard", "1973 US exits Vietnam; oil shock", "1974 Nixon resigns (Watergate)", "1979 Iran hostage crisis"],
1980: ["1981 Reagan presidency", "1987 INF Treaty with USSR"],
1990: ["1991 Gulf War; Cold War ends", "1994 NAFTA", "1990s Dot-com boom"],
2000: ["2001 9/11 attacks", "2003 Iraq invasion", "2008 Financial crisis; Obama elected"],
2010: ["2010 Affordable Care Act", "2011 Bin Laden killed", "2016 Trump elected"],
2020: ["2020 COVID-19 pandemic", "2021 Jan 6 Capitol attack; Afghanistan withdrawal", "2024 Trump elected again"],
}),
"Europe": ("7B2D26", "F2DCDB", {
1440: ["c.1440 Gutenberg's printing press"],
1450: ["1453 Ottomans take Constantinople", "1453 Hundred Years' War ends", "1455 Wars of the Roses begin"],
1460: ["1469 Ferdinand & Isabella marry → unified Spain"],
1470: ["1478 Spanish Inquisition"],
1480: ["1485 Tudors take the English throne"],
1490: ["1492 Granada falls — Reconquista complete; Jews expelled from Spain", "1494 Italian Wars begin"],
1500: ["c.1503 Mona Lisa", "1508 Michelangelo paints Sistine ceiling"],
1510: ["1513 Machiavelli's The Prince", "1517 Luther's 95 Theses → Reformation", "1519 Charles V becomes Holy Roman Emperor"],
1520: ["1521 Diet of Worms", "1526 Ottomans win at Mohács", "1529 Ottoman siege of Vienna"],
1530: ["1534 Henry VIII breaks with Rome"],
1540: ["1543 Copernicus: sun-centered universe", "1545 Council of Trent (Counter-Reformation)"],
1550: ["1555 Peace of Augsburg", "1558 Elizabeth I"],
1560: ["1562 French Wars of Religion", "1568 Dutch Revolt"],
1570: ["1571 Lepanto — Ottoman navy beaten", "1572 St. Bartholomew's Day Massacre"],
1580: ["1588 Spanish Armada defeated"],
1590: ["1598 Edict of Nantes"],
1600: ["1600 English East India Co.", "1602 Dutch VOC — first joint-stock giant"],
1610: ["1610 Galileo's telescope", "1618 Thirty Years' War begins"],
1640: ["1642 English Civil War", "1648 Peace of Westphalia → modern state system", "1649 Charles I executed"],
1650: ["1651 Hobbes' Leviathan", "1653 Cromwell rules"],
1660: ["1660 English monarchy restored", "1666 Great Fire of London"],
1680: ["1683 Ottomans turned back at Vienna", "1687 Newton's Principia", "1688 Glorious Revolution", "1689 English Bill of Rights; Locke"],
1690: ["1694 Bank of England"],
1700: ["1701 War of Spanish Succession", "1707 Great Britain formed", "1709 Poltava — Russia rises"],
1710: ["1713 Treaty of Utrecht"],
1720: ["1720 South Sea Bubble", "1721 Peter the Great proclaimed emperor"],
1740: ["1740 Frederick the Great; War of Austrian Succession"],
1750: ["1755 Lisbon earthquake", "1756 Seven Years' War"],
1760: ["1762 Catherine the Great; Rousseau's Social Contract", "1769 Watt's steam engine"],
1770: ["1772 First Partition of Poland", "1776 Adam Smith's Wealth of Nations"],
1780: ["1789 French Revolution; Rights of Man"],
1790: ["1793 Louis XVI executed; the Terror", "1799 Napoleon seizes power"],
1800: ["1804 Napoleon crowned emperor", "1805 Trafalgar & Austerlitz", "1806 Holy Roman Empire ends", "1807 Britain bans slave trade"],
1810: ["1812 Napoleon invades Russia", "1815 Waterloo; Congress of Vienna → Concert of Europe"],
1820: ["1821 Greek War of Independence", "1825 First public steam railway"],
1830: ["1830 July Revolution; Belgium independent", "1833 Britain abolishes slavery"],
1840: ["1845 Irish Famine", "1848 Revolutions across Europe; Communist Manifesto"],
1850: ["1853 Crimean War", "1859 Darwin's Origin of Species"],
1860: ["1861 Italy unified; Russia frees serfs", "1867 Austria-Hungary formed"],
1870: ["1870 Franco-Prussian War", "1871 German Empire; Paris Commune", "1878 Congress of Berlin"],
1880: ["1882 Triple Alliance", "1884 Berlin Conference carves up Africa"],
1890: ["1894 Franco-Russian Alliance", "1898 Germany builds navy"],
1900: ["1904 Entente Cordiale", "1905 Russian Revolution of 1905"],
1910: ["1914 WWI begins", "1917 Russian Revolution", "1918 Armistice; empires collapse", "1919 Treaty of Versailles"],
1920: ["1922 Mussolini; USSR formed", "1924 Stalin rises"],
1930: ["1933 Hitler takes power", "1936 Spanish Civil War", "1938 Munich Agreement", "1939 WWII begins"],
1940: ["1940 Fall of France", "1941 Germany invades USSR", "1944 D-Day", "1945 Germany surrenders; Holocaust revealed", "1949 NATO; Germany divided"],
1950: ["1953 Stalin dies", "1956 Hungarian uprising crushed", "1957 Treaty of Rome (EEC)"],
1960: ["1961 Berlin Wall", "1968 Prague Spring; Paris protests"],
1970: ["1975 Helsinki Accords; Franco dies"],
1980: ["1980 Solidarity in Poland", "1985 Gorbachev", "1986 Chernobyl", "1989 Berlin Wall falls"],
1990: ["1990 Germany reunified", "1991 USSR dissolves; Yugoslav wars", "1992 Maastricht → EU", "1995 Srebrenica"],
2000: ["2002 Euro notes & coins", "2004 EU expands east", "2008 Russia-Georgia war"],
2010: ["2010 Eurozone debt crisis", "2014 Russia annexes Crimea", "2015 Migrant crisis", "2016 Brexit vote"],
2020: ["2020 Brexit takes effect", "2022 Russia invades Ukraine"],
}),
"Asia & Middle East": ("8A5A00", "FBEBC8", {
1440: ["1443 Korea creates Hangul alphabet", "1449 Tumu Crisis — Ming emperor captured by Mongols"],
1450: ["1453 Ottomans make Constantinople their capital"],
1460: ["1467 Ōnin War → Japan's warring-states era"],
1490: ["1498 Vasco da Gama reaches India by sea"],
1500: ["1501 Safavid Persia founded"],
1510: ["1510 Portugal takes Goa", "1511 Portugal takes Malacca"],
1520: ["1520 Suleiman the Magnificent", "1526 Babur founds Mughal Empire"],
1540: ["1543 Portuguese guns reach Japan"],
1550: ["1556 Akbar the Great"],
1570: ["1571 Spain founds Manila"],
1590: ["1590 Hideyoshi unifies Japan", "1592 Japan invades Korea"],
1600: ["1600 Sekigahara", "1603 Tokugawa shogunate"],
1630: ["1632 Taj Mahal begun", "1639 Japan closes to the West"],
1640: ["1644 Ming falls; Qing dynasty (Manchu)"],
1660: ["1661 Kangxi Emperor"],
1680: ["1683 Qing take Taiwan"],
1700: ["1707 Aurangzeb dies → Mughal decline"],
1730: ["1739 Nader Shah sacks Delhi"],
1750: ["1757 Plassey — British East India Co. takes Bengal"],
1790: ["1793 China rebuffs British trade mission"],
1810: ["1819 Britain founds Singapore"],
1830: ["1839 First Opium War; Ottoman Tanzimat reforms"],
1840: ["1842 Treaty of Nanjing — Hong Kong to Britain"],
1850: ["1850 Taiping Rebellion (~20M dead)", "1853 Perry's 'black ships' reach Japan", "1857 Indian Rebellion", "1858 British Raj begins"],
1860: ["1860 Beijing's Summer Palace burned", "1868 Meiji Restoration — Japan modernizes"],
1870: ["1876 Japan forces Korea open", "1877 Victoria made Empress of India"],
1880: ["1885 Indian National Congress", "1887 French Indochina"],
1890: ["1894 First Sino-Japanese War", "1895 Japan takes Taiwan", "1898 US takes Philippines"],
1900: ["1900 Boxer Rebellion", "1905 Japan defeats Russia", "1908 Young Turk Revolution"],
1910: ["1910 Japan annexes Korea", "1911 Qing dynasty falls", "1916 Sykes-Picot carves up Middle East", "1919 May Fourth Movement"],
1920: ["1923 Atatürk's Turkish Republic", "1927 Chinese Civil War begins"],
1930: ["1930 Gandhi's Salt March", "1931 Japan seizes Manchuria", "1937 Japan invades China"],
1940: ["1941 Japan attacks Pearl Harbor", "1945 Hiroshima & Nagasaki", "1947 India & Pakistan partition", "1948 Israel founded", "1949 People's Republic of China"],
1950: ["1950 Korean War", "1954 Dien Bien Phu; Vietnam split", "1958 Great Leap Forward"],
1960: ["1966 Cultural Revolution", "1967 Six-Day War"],
1970: ["1973 Yom Kippur War; oil embargo", "1975 Saigon falls; Khmer Rouge", "1978 Deng's market reforms", "1979 Iranian Revolution; USSR invades Afghanistan"],
1980: ["1980 Iran-Iraq War", "1989 Tiananmen Square"],
1990: ["1991 Gulf War", "1997 Hong Kong returned; Asian Financial Crisis"],
2000: ["2001 China joins WTO; US invades Afghanistan", "2003 Iraq War"],
2010: ["2011 Arab Spring; Syrian civil war; Fukushima", "2012 Xi Jinping takes power", "2014 ISIS 'caliphate'"],
2020: ["2021 Taliban retake Afghanistan", "2023 Oct 7 attack; Gaza war"],
}),
"Africa": ("2E5E3A", "DCEBDF", {
1440: ["1441 Portuguese begin Atlantic slave trade from West Africa"],
1460: ["1464 Sonni Ali builds Songhai Empire"],
1480: ["1482 Portuguese build Elmina Castle", "1488 Dias rounds Cape of Good Hope"],
1490: ["1493 Askia Muhammad — Songhai's peak; Timbuktu flourishes"],
1500: ["1505 Portuguese sack Kilwa (Swahili coast)"],
1510: ["1517 Ottomans conquer Egypt"],
1520: ["1526 Kongo's King Afonso protests slave trade", "1529 Adal invades Ethiopia"],
1590: ["1591 Morocco destroys Songhai"],
1650: ["1652 Dutch found Cape Town"],
1690: ["1698 Omani Arabs take Mombasa — Swahili coast shifts to Oman"],
1700: ["c.1701 Asante Empire rises"],
1790: ["1795 Britain takes the Cape"],
1800: ["1804 Sokoto Caliphate", "1807 Britain bans slave trade"],
1810: ["1818 Shaka builds Zulu kingdom"],
1820: ["1822 Liberia founded"],
1830: ["1830 France invades Algeria", "1835 Boer Great Trek"],
1840: ["1840 Oman moves capital to Zanzibar"],
1860: ["1869 Suez Canal opens"],
1870: ["1873 Zanzibar slave market closed", "1879 Anglo-Zulu War"],
1880: ["1882 Britain occupies Egypt", "1884 Berlin Conference — Scramble for Africa", "1885 Congo Free State; German East Africa"],
1890: ["1896 Ethiopia defeats Italy at Adwa", "1896 Anglo-Zanzibar War", "1899 Boer War"],
1900: ["1904 Herero & Nama genocide", "1905 Maji Maji Rebellion (Tanganyika)", "1908 Belgium takes Congo from Leopold"],
1910: ["1910 Union of South Africa", "1914 WWI East Africa campaign"],
1920: ["1922 Egypt nominally independent"],
1930: ["1935 Italy invades Ethiopia"],
1940: ["1948 Apartheid begins"],
1950: ["1952 Mau Mau uprising (Kenya)", "1954 Algerian War", "1956 Suez Crisis", "1957 Ghana independent"],
1960: ["1960 'Year of Africa' — 17 nations independent", "1961 Lumumba killed; Tanganyika independent", "1963 OAU founded; Kenya independent", "1964 Tanzania formed", "1967 Biafran War; Arusha Declaration"],
1970: ["1974 Haile Selassie overthrown", "1975 Angola & Mozambique independent", "1979 Tanzania ousts Idi Amin"],
1980: ["1980 Zimbabwe independent", "1984 Ethiopian famine"],
1990: ["1990 Mandela freed", "1994 Rwandan genocide; Mandela president", "1996 Congo wars begin"],
2000: ["2002 African Union", "2003 Darfur"],
2010: ["2011 Arab Spring (Tunisia, Egypt, Libya); South Sudan independent", "2014 Ebola outbreak"],
2020: ["2020 Tigray war", "2021 Sahel coups begin", "2023 Sudan civil war"],
}),
"Latin America & Caribbean": ("5E2A6E", "EBDDF0", {
1490: ["1492 Columbus reaches the Caribbean", "1494 Treaty of Tordesillas splits world"],
1500: ["1500 Cabral claims Brazil for Portugal"],
1510: ["1513 Balboa sees the Pacific", "1519 Cortés lands in Mexico"],
1520: ["1521 Aztec capital Tenochtitlan falls"],
1530: ["1532 Pizarro captures Inca emperor Atahualpa"],
1540: ["1545 Potosí silver mines"],
1560: ["1565 Manila galleon trade links Mexico & Asia"],
1570: ["1572 Last Inca stronghold falls"],
1690: ["1693 Brazilian gold rush"],
1780: ["1780 Túpac Amaru II rebellion"],
1790: ["1791 Haitian Revolution begins"],
1800: ["1804 Haiti independent — first Black republic", "1808 Portuguese court flees to Brazil"],
1810: ["1810 Hidalgo's revolt — Mexico's war of independence", "1816 Argentina independent", "1819 Bolívar wins at Boyacá"],
1820: ["1821 Mexico independent", "1822 Brazil independent", "1824 Ayacucho ends Spanish rule"],
1830: ["1830 Gran Colombia breaks apart"],
1840: ["1848 Mexico loses half its land to US"],
1860: ["1862 French invade Mexico", "1864 Paraguayan War", "1867 Emperor Maximilian executed"],
1870: ["1876 Porfirio Díaz dictatorship"],
1880: ["1886 Cuba ends slavery", "1888 Brazil abolishes slavery", "1889 Brazil becomes republic"],
1890: ["1895 Cuban War of Independence", "1898 Spain loses Cuba & Puerto Rico"],
1900: ["1903 Panama splits from Colombia", "1904 Roosevelt Corollary"],
1910: ["1910 Mexican Revolution", "1914 Panama Canal opens"],
1930: ["1930 Vargas takes power in Brazil", "1938 Mexico nationalizes oil"],
1940: ["1946 Perón in Argentina"],
1950: ["1954 US-backed coup in Guatemala", "1959 Cuban Revolution"],
1960: ["1961 Bay of Pigs", "1962 Cuban Missile Crisis", "1964 Brazil military coup", "1967 Che killed in Bolivia"],
1970: ["1973 Pinochet coup in Chile", "1976 Argentina's Dirty War", "1979 Sandinista revolution"],
1980: ["1982 Falklands War; debt crisis", "1989 US invades Panama"],
1990: ["1994 NAFTA; Zapatista uprising", "1999 Chávez in Venezuela"],
2000: ["2001 Argentina defaults", "2003 Lula in Brazil"],
2010: ["2010 Haiti earthquake", "2014 Venezuela crisis deepens", "2016 Colombia-FARC peace deal"],
2020: ["2021 Haiti's president assassinated", "2023 Milei elected in Argentina"],
}),
}

wb = Workbook()
ws = wb.active
ws.title = "Timeline"
F = "Arial"
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap_c = Alignment(wrap_text=True, vertical="center", horizontal="center")
wrap_t = Alignment(wrap_text=True, vertical="top", horizontal="left")

ws.column_dimensions["A"].width = 22
for d, c in col.items():
    ws.column_dimensions[get_column_letter(c)].width = 30

def label(r, text, color):
    cell = ws.cell(r, 1, text)
    cell.font = Font(name=F, bold=True, color="FFFFFF", size=11)
    cell.fill = PatternFill("solid", fgColor=color)
    cell.alignment = wrap_c
    cell.border = border

# Row 1: decades
label(1, "DECADE", "222222")
for d, c in col.items():
    cell = ws.cell(1, c, f"{d}s")
    cell.font = Font(name=F, bold=True, color="FFFFFF", size=13)
    cell.fill = PatternFill("solid", fgColor="222222")
    cell.alignment = wrap_c
ws.row_dimensions[1].height = 26

def band(r, spans, default_fill, font_color, bold, size):
    for s in spans:
        a, b, text = s[0], s[1], s[2]
        fill = s[3] if len(s) > 3 else default_fill
        c1, c2 = col[a], col[b]
        if c2 > c1:
            ws.merge_cells(start_row=r, start_column=c1, end_row=r, end_column=c2)
        cell = ws.cell(r, c1, text)
        cell.font = Font(name=F, bold=bold, color=font_color, size=size)
        cell.alignment = wrap_c
        for c in range(c1, c2 + 1):
            ws.cell(r, c).fill = PatternFill("solid", fgColor=fill)
            ws.cell(r, c).border = border

label(2, "ERA", "444444"); band(2, ERAS, None, "FFFFFF", True, 12); ws.row_dimensions[2].height = 32
label(3, "GLOBAL ORDER", "666666"); band(3, EXPLORE, None, "222222", True, 10); ws.row_dimensions[3].height = 34
label(4, "DEFINING CONFLICTS", "666666"); band(4, CONFLICTS, "EFEFEF", "222222", False, 10); ws.row_dimensions[4].height = 44
label(5, "TECH & IDEAS", "666666"); band(5, TECH, "FFF7E0", "5A4300", False, 10); ws.row_dimensions[5].height = 36

long_rows = []
r = 6
for name, (dark, light, events) in REGIONS.items():
    label(r, name.upper(), dark)
    maxlines = 1
    for d, c in col.items():
        cell = ws.cell(r, c)
        cell.border = border
        evs = events.get(d, [])
        if evs:
            cell.value = "\n".join("• " + e for e in evs)
            cell.fill = PatternFill("solid", fgColor=light)
            lines = sum(1 + len(e) // 34 for e in evs)
            maxlines = max(maxlines, lines)
            for e in evs:
                yr = e.split(" ")[0].replace("c.", "").replace("s", "")
                long_rows.append((int(yr[:4]), name, e.split(" ", 1)[1], d))
        cell.font = Font(name=F, size=10)
        cell.alignment = wrap_t
    ws.row_dimensions[r].height = min(15 * maxlines + 6, 400)
    r += 1

ws.freeze_panes = "B2"
ws.sheet_view.zoomScale = 90

# Sheet 2: flat list
ws2 = wb.create_sheet("All Events (sortable)")
hdr = ["Year", "Decade", "Region", "Event"]
for i, h in enumerate(hdr, 1):
    c = ws2.cell(1, i, h)
    c.font = Font(name=F, bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor="222222")
for i, (y, reg, ev, d) in enumerate(sorted(long_rows), 2):
    ws2.cell(i, 1, y); ws2.cell(i, 2, f"{d}s"); ws2.cell(i, 3, reg); ws2.cell(i, 4, ev)
    for j in range(1, 5):
        ws2.cell(i, j).font = Font(name=F, size=10)
ws2.column_dimensions["A"].width = 8
ws2.column_dimensions["B"].width = 9
ws2.column_dimensions["C"].width = 28
ws2.column_dimensions["D"].width = 70
ws2.freeze_panes = "A2"
ws2.auto_filter.ref = f"A1:D{len(long_rows)+1}"

wb.save("World_History_Timeline_1444-Present.xlsx")
print(len(long_rows), "events")
