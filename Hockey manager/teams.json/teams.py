import json 

teams_data = [
    {
        "name": "Dinamo Moscow",
        "players": [
            {"name": "Nick Gusev", "position": "Forward", "skill": 92},
            {"name": "Semen Der-Arguchincev", "position": "Forward", "skill": 88},
            {"name": "Maxim Comtois", "position": "Forward", "skill": 90},
            {"name": "Sedrik Packett", "position": "Forward", "skill": 90},
            {"name": "Igor Ozhiganov", "position": "Defender", "skill": 87},
            {"name": "Artem Sergeev", "position": "Defender", "skill": 88},
            {"name": "Daniil Pylenkov", "position": "Defender", "skill": 85},
            {"name": "Vladislav Podyapolskiy", "position": "Goalkeeper", "skill": 90}
        ]
    },
    {
        "name": "Spartak",
        "players": [
            {"name": "Pavel Poryadin", "position": "Forward", "skill": 91},
            {"name": "Egor Filin", "position": "Forward", "skill": 87},
            {"name": "Ignat Korotkih", "position": "Forward", "skill": 85},
            {"name": "Daniil Gutik", "position": "Forward", "skill": 88},
            {"name": "Dmitriy Vishnevskiy", "position": "Defender", "skill": 87},
            {"name": "Daniil Ivanov", "position": "Defender", "skill": 86},
            {"name": "Andrey Mironov", "position": "Defender", "skill": 88},
            {"name": "Evgeniy Volokhin", "position": "Goalkeeper", "skill": 84}
        ]
    },
    {
        "name": "SKA",
        "players": [
            {"name": "Nikolay Goldobin", "position": "Forward", "skill": 91},
            {"name": "Matvey Korotkiy", "position": "Forward", "skill": 88},
            {"name": "Marat Hairulin", "position": "Forward", "skill": 89},
            {"name": "Sergey Plotnikov", "position": "Forward", "skill": 86},
            {"name": "Trevor Murphy", "position": "Defender", "skill": 88},
            {"name": "Sergey Sapego", "position": "Defender", "skill": 88},
            {"name": "Andrey Pedan", "position": "Defender", "skill": 89},
            {"name": "Sergey Ivanov", "position": "Goalkeeper", "skill": 85}
        ]
    },
    {
        "name": "Torpedo",
        "players": [
            {"name": "Egor Vinogradov", "position": "Forward", "skill": 87},
            {"name": "Vladimir Tkachyov", "position": "Forward", "skill": 89},
            {"name": "Vasiliy Atanasov", "position": "Forward", "skill": 91},
            {"name": "Maxim Letunov", "position": "Forward", "skill": 90},
            {"name": "Mihail Naumenkov", "position": "Defender", "skill": 87},
            {"name": "Denis Aleksandrov", "position": "Defender", "skill": 86},
            {"name": "Bogdan Konyushkov", "position": "Defender", "skill": 89},
            {"name": "Dmitriy Shugayev", "position": "Goalkeeper", "skill": 86}
        ]
    },
    {
        "name": "CSKA",
        "players": [
            {"name": "Denis Zernov", "position": "Forward", "skill": 90},
            {"name": "Prokhor Poltapov", "position": "Forward", "skill": 89},
            {"name": "Klim Kostin", "position": "Forward", "skill": 89},
            {"name": "Ivan Drozdov", "position": "Forward", "skill": 88},
            {"name": "Jeremy Roy", "position": "Defender", "skill": 88},
            {"name": "Nick Nesterov", "position": "Defender", "skill": 88},
            {"name": "Nick Ebert", "position": "Defender", "skill": 90},
            {"name": "Alex Privalov", "position": "Goalkeeper", "skill": 88}
        ]
    },
    {
        "name": "Severstal",
        "players": [
            {"name": "Danil Aimurzin", "position": "Forward", "skill": 89},
            {"name": "Adam Lishka", "position": "Forward", "skill": 88},
            {"name": "Ivan Abrosimov", "position": "Forward", "skill": 89},
            {"name": "Ilya Ivanzov", "position": "Forward", "skill": 87},
            {"name": "Vladimir Grudinin", "position": "Defender", "skill": 88},
            {"name": "Ivan Ershov", "position": "Defender", "skill": 88},
            {"name": "Nick Kamalov", "position": "Defender", "skill": 87},
            {"name": "Konstantin Shostak", "position": "Goalkeeper", "skill": 90}
        ]
    },
    {
        "name": "Dinamo Minsk",
        "players": [
            {"name": "Sam Anas", "position": "Forward", "skill": 93},
            {"name": "Alex Limozh", "position": "Forward", "skill": 90},
            {"name": "Rayan Spuner", "position": "Forward", "skill": 90},
            {"name": "Vitaliy Pinchuk", "position": "Forward", "skill": 90},
            {"name": "Kristian Henkel", "position": "Defender", "skill": 89},
            {"name": "Pavel Denisov", "position": "Defender", "skill": 87},
            {"name": "Darren Diz", "position": "Defender", "skill": 86},
            {"name": "Zack Fukale", "position": "Goalkeeper", "skill": 89}
        ]
    },
    {
        "name": "Lokomotiv",
        "players": [
            {"name": "Alex Radulov", "position": "Forward", "skill": 90},
            {"name": "Egor Surin", "position": "Forward", "skill": 92},
            {"name": "Artur Kayumov", "position": "Forward", "skill": 91},
            {"name": "Pavel Kraskovskiy", "position": "Forward", "skill": 90},
            {"name": "Martin Gernat", "position": "Defender", "skill": 90},
            {"name": "Aleksey Bereglazov", "position": "Defender", "skill": 90},
            {"name": "Alex Yelesin", "position": "Defender", "skill": 90},
            {"name": "Daniil Isaev", "position": "Goalkeeper", "skill": 91}
        ]
    },
    {
        "name": "Sibir",
        "players": [
            {"name": "Arkhip Nekolenko", "position": "Forward", "skill": 84},
            {"name": "Ivan Klimovich", "position": "Forward", "skill": 85},
            {"name": "Sergey Shirokov", "position": "Forward", "skill": 87},
            {"name": "Teilor Beck", "position": "Forward", "skill": 88},
            {"name": "Egor Alanov", "position": "Defender", "skill": 86},
            {"name": "Mihail Orlov", "position": "Defender", "skill": 85},
            {"name": "Egor Zaizev", "position": "Defender", "skill": 85},
            {"name": "Anton Krasotkin", "position": "Goalkeeper", "skill": 86}
        ]
    },
    {
        "name": "Nephtehimik",
        "players": [
            {"name": "Nick Artamonov", "position": "Forward", "skill": 84},
            {"name": "Nick Horuzhev", "position": "Forward", "skill": 85},
            {"name": "Alex Dergachyov", "position": "Forward", "skill": 85},
            {"name": "Nick Popugayev", "position": "Forward", "skill": 85},
            {"name": "Dinar Hafizulin", "position": "Defender", "skill": 84},
            {"name": "Luka Profaka", "position": "Defender", "skill": 84},
            {"name": "Nick Hlystov", "position": "Defender", "skill": 83},
            {"name": "Yaroslav Ozolin", "position": "Goalkeeper", "skill": 84}
        ]
    },
    {
        "name": "Traktor",
        "players": [
            {"name": "Joshua Livo", "position": "Forward", "skill": 88},
            {"name": "Mihail Grigorenko", "position": "Forward", "skill": 87},
            {"name": "Vasiliy Glotov", "position": "Forward", "skill": 88},
            {"name": "Alex Kadeykin", "position": "Forward", "skill": 88},
            {"name": "Sergey Telegin", "position": "Defender", "skill": 87},
            {"name": "Jordan Gross", "position": "Defender", "skill": 85},
            {"name": "Gregor Dronov", "position": "Defender", "skill": 86},
            {"name": "Sergey Mylnikov", "position": "Goalkeeper", "skill": 85}
        ]
    },
    {
        "name": "Salavat Yulaev",
        "players": [
            {"name": "Sheldon Rempal", "position": "Forward", "skill": 89},
            {"name": "Evgeniy Kuznetsov", "position": "Forward", "skill": 86},
            {"name": "Alex Zharovskiy", "position": "Forward", "skill": 88},
            {"name": "Artem Gorshkov", "position": "Forward", "skill": 89},
            {"name": "Evgeniy Kulik", "position": "Defender", "skill": 86},
            {"name": "Ildan Gazimov", "position": "Defender", "skill": 86},
            {"name": "Alexey Vasilevskiy", "position": "Defender", "skill": 87},
            {"name": "Semen Vyazovoy", "position": "Goalkeeper", "skill": 87}
        ]
    },
    {
        "name": "Avtomobilist",
        "players": [
            {"name": "Daniel Sprong", "position": "Forward", "skill": 93},
            {"name": "Anatoliy Golyshev", "position": "Forward", "skill": 89},
            {"name": "Stephan Da Costa", "position": "Forward", "skill": 90},
            {"name": "Alex Sharov", "position": "Forward", "skill": 87},
            {"name": "Nick Tryamkin", "position": "Defender", "skill": 89},
            {"name": "Kirill Vorobyov", "position": "Defender", "skill": 87},
            {"name": "Sergey Zborovskiy", "position": "Defender", "skill": 88},
            {"name": "Evgeniy Alikin", "position": "Goalkeeper", "skill": 92}
        ]
    },
    {
        "name": "Ak Bars",
        "players": [
            {"name": "Dmitriy Yashkin", "position": "Forward", "skill": 90},
            {"name": "Ilya Saphonov", "position": "Forward", "skill": 91},
            {"name": "Nick Dynyak", "position": "Forward", "skill": 90},
            {"name": "Artem Galimov", "position": "Forward", "skill": 89},
            {"name": "Alexey Marchenko", "position": "Defender", "skill": 88},
            {"name": "Stepan Falkovskiy", "position": "Defender", "skill": 89},
            {"name": "Nick Lyamkin", "position": "Defender", "skill": 91},
            {"name": "Timur Bilyalov", "position": "Goalkeeper", "skill": 89}
        ]
    },
    {
        "name": "Avangard",
        "players": [
            {"name": "Andrew Poturalski", "position": "Forward", "skill": 89},
            {"name": "Okulov Konstantin", "position": "Forward", "skill": 90},
            {"name": "Nail Yakupov", "position": "Forward", "skill": 89},
            {"name": "Michael Mcleod", "position": "Forward", "skill": 92},
            {"name": "Marsel Ibragimov", "position": "Defender", "skill": 88},
            {"name": "Damir Sharipzyanov", "position": "Defender", "skill": 91},
            {"name": "Vyacheslav Voinov", "position": "Defender", "skill": 89},
            {"name": "Nick Serebryakov", "position": "Goalkeeper", "skill": 90}
        ]
    },
    {
        "name": "Metalurg",
        "players": [
            {"name": "Roman Kanzerov", "position": "Forward", "skill": 94},
            {"name": "Dmitriy Silantiev", "position": "Forward", "skill": 90},
            {"name": "Alex Petunin", "position": "Forward", "skill": 91},
            {"name": "Daniil Vovchenko", "position": "Forward", "skill": 89},
            {"name": "Egor Yakovlev", "position": "Defender", "skill": 87},
            {"name": "Valeriy Orekhov", "position": "Defender", "skill": 89},
            {"name": "Robin Press", "position": "Defender", "skill": 89},
            {"name": "Ilya Nabokov", "position": "Goalkeeper", "skill": 92}
        ]
    }
]


with open("teams.json", "w", encoding = "utf-8") as f:
    json.dump(teams_data, f, ensure_ascii = False, indent = 4)