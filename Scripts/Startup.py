import tkinter
from tkinter import ttk
import subprocess
import time
import threading

province_dict = {
        "Alberta":"1",
        "British Columbia":"2",
        "Manitoba":"3",
        "New Brunswick":"4",
        "Newfoundland":"5",
        "Nova Scotia":"6",
        "Ontario (A - L)":"7",
        "Ontario (M - Z)":"8",
        "Prince Edward Island":"9",
        "Qu\u00e9bec":"10",
        "Saskatchewan":"11",
        "Territories":"12"
    }

city_dict = {
        "1": {
            "Banff / Canmore":"1",
            "Calgary":"2",
            "Edmonton Area":"3",
            "Fort McMurray":"4",
            "Grande Prairie":"5",
            "Lethbridge":"6",
            "Lloydminster":"7",
            "Medicine Hat":"8",
            "Red Deer":"9"
        },
        "2": {
            "Cariboo Area":"1",
            "Comox Valley Area":"2",
            "Cowichan Valley / Duncan":"3",
            "Cranbrook":"4",
            "Fraser Valley":"5",
            "Greater Vancouver Area":"6",
            "Kamloops":"7",
            "Kelowna":"8",
            "Nanaimo":"9",
            "Nelson":"10",
            "Peace River Area":"11",
            "Port Alberni / Oceanside":"12",
            "Port Hardy / Port McNeill":"13",
            "Powell River District":"14",
            "Prince George":"15",
            "Revelstoke":"16",
            "Skeena-Bulkley Area":"17",
            "Sunshine Coast":"18",
            "Vernon":"19",
            "Victoria":"20",
            "Whistler":"21"
        },
        "3": {
            "Brandon Area":"1",
            "Flin Flon":"2",
            "Thompson":"3",
            "Winnipeg":"4"
        },
        "4": {
            "Bathurst":"1",
            "Edmundston":"2",
            "Fredericton":"3",
            "Miramichi":"4",
            "Moncton":"5",
            "Saint John":"6"
        },
        "5": {
            "Corner Brook":"1",
            "Gander":"2",
            "Labrador":"3",
            "St. John's":"4"
        },
        "6": {
            "Annapolis Valley":"1",
            "Bridgewater":"2",
            "Cape Breton":"3",
            "Halifax":"4",
            "New Glasgow":"5",
            "Truro":"6",
            "Yarmouth":"7"
        },
        "7": {
            "Barrie":"1",
            "Belleville Area":"2",
            "Brantford":"3",
            "Brockville":"4",
            "Chatham-Kent":"5",
            "Cornwall":"6",
            "Guelph":"7",
            "Hamilton":"8",
            "Kapuskasing":"9",
            "Kenora":"10",
            "Kingston Area":"11",
            "Kitchener Area":"12",
            "Leamington":"13",
            "London":"14"
        },
        "8": {
            "Muskoka":"1",
            "Norfolk County":"2",
            "North Bay":"3",
            "Ottawa / Gatineau Area":"4",
            "Owen Sound":"5",
            "Peterborough Area":"6",
            "Renfrew County Area":"7",
            "Sarnia Area":"8",
            "Sault Ste. Marie":"9",
            "St. Catharines":"10",
            "Sudbury":"11",
            "Thunder Bay":"12",
            "Timmins":"13",
            "Toronto (GTA)":"14",
            "Windsor Region":"15",
            "Woodstock":"16"
        },
        "9": {
            "Prince Edward Island":"1"
        },
        "10": {
            "Abitibi-T\u00e9miscamingue":"1",
            "Baie-Comeau":"2",
            "Centre-du-Quebec":"3",
            "Chaudi\u00e8re-Appalaches":"4",
            "Chibougamau / Northern Qu\u00e9bec":"5",
            "Gasp\u00e9":"6",
            "Granby":"7",
            "Greater Montr\u00e9al":"8",
            "Lanaudi\u00e8re":"9",
            "Laurentides":"10",
            "Mauricie":"11",
            "Qu\u00e9bec City":"12",
            "Rimouski / Bas-St-Laurent":"13",
            "Saguenay-Lac-Saint-Jean":"14",
            "Saint-Hyacinthe":"15",
            "Saint-Jean-sur-Richelieu":"16",
            "Sept-\u00celes":"17",
            "Sherbrooke":"18"
        },
        "11": {
            "La Ronge":"1",
            "Meadow Lake":"2",
            "Nipawin":"3",
            "Prince Albert":"4",
            "Regina Area":"5",
            "Saskatoon":"6",
            "Swift Current":"7"
        },
        "12": {
            "Northwest Territories":"1",
            "Nunavut":"2",
            "Yukon":"3"
        }
    }

# Initializing Application Window
window = tkinter.Tk()
window.title("Kijiji Web Scraping")
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth()/2 - windowWidth)
positionDown = int(window.winfo_screenheight()/2 - windowHeight)
 
# Positions the window in the center of the page.
window.geometry("+{}+{}".format(positionRight, positionDown))
window.geometry('500x400') 
window['background'] = '#e6e6e6'

keywordsCount = 8
count = 0
keywords = {}

# Method For Changing City Depending on Province
def enableCities(event):

    # City Label And ComboBox 
    if province_choosen.get().strip() == "Alberta":
        city_choosen['values'] = (
            ' Banff / Canmore',' Calgary',' Edmonton Area',' Fort McMurray',' Grande Prairie',' Lethbridge',
            ' Lloydminster',' Medicine Hat',' Red Deer'
        )
    elif province_choosen.get().strip() == "British Columbia":  
        city_choosen['values'] = (
            ' Cariboo Area', ' Comox Valley Area',' Cowichan Valley / Duncan',' Cranbrook',' Fraser Valley',' Greater Vancouver Area', 
            ' Kamloops',' Kelowna',' Nanaimo',' Nelson',' Peace River Area',' Port Alberni / Oceanside',' Port Hardy / Port McNeill',' Powell River District',
            ' Prince George',' Revelstoke',' Skeena-Bulkley Area',' Sunshine Coast',' Vernon',' Victoria',' Whistler'
        )
    elif province_choosen.get().strip() == "Manitoba":  
        city_choosen['values'] = (
            ' Brandon Area',' Flin Flon',' Thompson',' Winnipeg'
        )
    elif province_choosen.get().strip() == "New Brunswick":
        city_choosen['values'] = (
            ' Bathurst',' Edmundston',' Fredericton',' Miramichi',' Moncton',' Saint John'
        )
    elif province_choosen.get().strip() == "Newfoundland":
        city_choosen['values'] = (
            ' Corner Brook',' Gander',' Labrador'," St. John's",' Moncton',' Saint John'
        )
    elif province_choosen.get().strip() == "Nova Scotia":
        city_choosen['values'] = (
            ' Annapolis Valley',' Bridgewater',' Cape Breton'," Halifax",' New Glasgow',' Truro',' Yarmouth'
        )
    elif province_choosen.get().strip() == "Ontario (A - L)":
        city_choosen['values'] = (
            ' Barrie',' Belleville Area',' Brantford'," Brockville",' Chatham-Kent',' Cornwall',
            ' Guelph',' Hamilton',' Kapuskasing',' Kenora',' Kingston Area',' Kitchener Area',
            ' Leamington',' London'
        )
    elif province_choosen.get().strip() == "Ontario (M - Z)":
        city_choosen['values'] = (
            ' Muskoka',' Norfolk County',' North Bay'," Ottawa / Gatineau Area",' Owen Sound',' Peterborough Area',
            ' Renfrew County Area',' Sarnia Area',' Sault Ste. Marie',' St. Catharines',' Sudbury',' Thunder Bay',
            ' Timmins',' Toronto (GTA)',' Windsor Region',' Woodstock'
        )
    elif province_choosen.get().strip() == "Prince Edward Island":
        city_choosen['values'] = (
            ' Prince Edward Island'
        )
    elif province_choosen.get().strip() == "Qu\u00e9bec":
        city_choosen['values'] = (
            ' Abitibi-T\u00e9miscamingue',' Baie-Comeau',' Centre-du-Quebec'," Chaudi\u00e8re-Appalaches",' Chibougamau / Northern Qu\u00e9bec',' Gasp\u00e9',
            ' Granby',' Greater Montr\u00e9al',' Lanaudi\u00e8re',' Laurentides',' Mauricie',' Qu\u00e9bec City',
            ' Rimouski / Bas-St-Laurent',' Saguenay-Lac-Saint-Jean',' Saint-Hyacinthe',' Saint-Jean-sur-Richelieu',' Sept-\u00celes',' Sherbrooke'
        )
    elif province_choosen.get().strip() == "Saskatchewan":
        city_choosen['values'] = (
            ' La Ronge',' Meadow Lake',' Nipawin'," Prince Albert",' Regina Area',' Saskatoon',' Swift Current'
        )
    elif province_choosen.get().strip() == "Territories":
        city_choosen['values'] = (
            ' Northwest Territories',' Nunavut',' Yukon'
        )
    
    ttk.Label(window, text = "City :", font = ("Calibri", 15)).grid(column = 0,row = 7, padx = 10, pady = 10)
    city_choosen.grid(column = 1, row = 7) 
    city_choosen.current()  

def execute_scraping():
    global count
    btn.destroy()
    label = ttk.Label(window, text = "Process Running......", font = ("Calibri", 15))
    label.place(relx="0.35",rely="0.7")
    progressBar = ttk.Progressbar(window, orient='horizontal', length=400, mode='determinate')
    progressBar.place(relx="0.1",rely="0.8")
    progressBar.start(10)

    finalKeywords = ''
    if count >= 0:
        finalKeywords += keywords["0"].get()
    if count >= 1:
        finalKeywords += ','
        finalKeywords += keywords["1"].get()
    if count == 2:
        finalKeywords += ','
        finalKeywords += keywords["2"].get()

    def destroy_window():
        window.destroy()

    if advertisement_type.get().strip() == "Wanted":
        def subProcess():
            subprocess.check_call("python Scraping.py " + str(province_dict[province_choosen.get().strip()]) + " " + str((city_dict[province_dict[province_choosen.get().strip()]])[city_choosen.get().strip()]) + " w " + str(finalKeywords), shell=True)
            label = ttk.Label(window, text = "Process Completed", font = ("Calibri", 15))
            label.place(relx="0.35",rely="0.7")
            progressBar.destroy()
            progressBBar = ttk.Progressbar(window, orient='horizontal', length=400, mode='determinate')
            progressBBar.place(relx="0.1",rely="0.8")
            progressBBar['value'] = 100
            bbtn = ttk.Button(window, text="Ok",command=destroy_window)
            bbtn.place(relx="0.4",rely="0.9")
        
        scriptRun = threading.Thread(target=subProcess, args=())
        scriptRun.start()

    elif advertisement_type.get().strip() == "Offering":
        subprocess.check_call("python Scraping.py " + str(province_dict[province_choosen.get().strip()]) + " " + str((city_dict[province_dict[province_choosen.get().strip()]])[city_choosen.get().strip()]) + " o " + str(finalKeywords), shell=True)
        label = ttk.Label(window, text = "Process Completed", font = ("Calibri", 15))
        label.place(relx="0.35",rely="0.7")
        progressBar.destroy()
        progressBar = ttk.Progressbar(window, orient='horizontal', length=400, mode='determinate')
        progressBar.place(relx="0.1",rely="0.8")
        progressBar['value'] = 100
        bbtn = ttk.Button(window, text="Ok",command=destroy_window)
        bbtn.place(relx="0.4",rely="0.9")   

def addKeyword():
    global keywordsCount
    global count
    if keywordsCount < 10:
        count +=1
        keywordsCount += 1
        keywords[str(count)] = ttk.Entry(window, width = 35)
        keywords[str(count)].grid(column = 1,row = keywordsCount, pady = 10)

def enableButton(event):
    ttk.Label(window, text = "Keyword :", font = ("Calibri", 15)).grid(column = 0,row = 8, padx = 10, pady = 10)
    keywords[str(count)] = ttk.Entry(window, width = 35)
    keywords[str(count)].grid(column = 1,row = 8)
    bbtn = ttk.Button(window, text="Add", command=addKeyword)
    bbtn.place(relx="0.1",rely="0.5")
    btn.place(relx="0.4",rely="0.7")

def enableProvince(event): 
    ttk.Label(window, text = "Province :", font = ("Calibri", 15)).grid(column = 0,row = 6, padx = 10, pady = 10) 
    province_choosen.grid(column = 1, row = 6) 
    province_choosen.current()


# Advertisement Type : Dropdown, Values And Positioning
ttk.Label(window, text = "Advertisement Type :", font = ("Calibri", 15)).grid(column = 0,row = 5, padx = 10, pady = 10)   
advertisement_type = ttk.Combobox(window, width = 35, height = 30, textvariable = tkinter.StringVar(), state="readonly")
advertisement_type.bind("<<ComboboxSelected>>", enableProvince)
advertisement_type['values'] = (' Wanted', ' Offering')
advertisement_type.grid(column = 1, row = 5) 
advertisement_type.current()

# Province : Dropdown, Values, Positioning and Method Calling To Enable Cities
province_choosen = ttk.Combobox(window, width = 35, height = 30, textvariable = tkinter.StringVar(), state="readonly") 
province_choosen.bind("<<ComboboxSelected>>", enableCities)
province_choosen['values'] = (
    ' Alberta',' British Columbia',' Manitoba',' New Brunswick',' Newfoundland',' Nova Scotia',
    ' Ontario (A - L)',' Ontario (M - Z)',' Prince Edward Island',' Qu\u00e9bec',' Saskatchewan',' Territories'
)

# City : Dropdown, Values, Positioning
city_choosen = ttk.Combobox(window, width = 35, height = 30, textvariable = tkinter.StringVar(), state="readonly")
city_choosen.bind("<<ComboboxSelected>>", enableButton)

btn = ttk.Button(window, text="Start",command=execute_scraping)

window.mainloop()