from utils import with_driver, without_driver
import json

SITE_URL = 'https://www.wheel-size.com'


def get_brands():
    _bs = without_driver(SITE_URL)
    brands = _bs.find_all('a', {'itemprop': 'itemListElement'})
    if not brands:
        _bs = with_driver(SITE_URL)
        brands = _bs.find_all('a', {'itemprop': 'itemListElement'})
    return {b.get_text(): b.get('href') for b in brands}


def get_id(link):
    _bs = without_driver(SITE_URL + link)
    markets = _bs.find_all('section', {'class': 'models-list'})
    if not markets:
        _bs = with_driver(SITE_URL + link)
        markets = _bs.find_all('section', {'class': 'models-list'})
    if 'market' not in markets[0].find('h4').get_text().strip().lower():
        market_type = 'None'
        tag_view = markets[0].find('div', {'class': 'large-tag-view'})
        id_list = [a.get('href') for a in tag_view.find_all('a', {'class': 'd-inline'})]
        return {market_type: id_list}
    else:
        t_dict = {}
        for market in markets:
            try:
                market_type = market.find('h4').get_text().strip()
                if 'market' not in market_type.lower():
                    continue
                tag_view = market.find('div', {'class': 'large-tag-view'})
                id_list = [a.get('href') for a in tag_view.find_all('a', {'class': 'd-inline'})]
                market_type = market_type.split("(")[1].replace(")", '').strip()
                t_dict[market_type] = id_list
            except Exception as e:
                print(e)
                continue
        return t_dict


# brands_list = ['Acura', 'Alfa Romeo', 'Alpine', 'ARO', 'Aston Martin', 'Audi', 'BAIC', 'Bentley', 'BMW',
#                'BMW Alpina',
#                'Borgward', 'Brilliance', 'Bugatti', 'Buick', 'BYD', 'Cadillac', 'Changan', 'Chery', 'Chevrolet',
#                'Chrysler', 'Citroën', 'Cupra', 'Dacia', 'Daewoo', 'Daihatsu', 'Datsun', 'Dodge', 'Dongfeng', 'DS',
#                'Eagle', 'Exeed', 'FAW', 'Ferrari', 'Fiat', 'Fisker', 'Force', 'Ford', 'Foton', 'GAC', 'GAZ',
#                'Geely',
#                'Genesis', 'GEO', 'GMC', 'Great Wall', 'Haval', 'Hindustan', 'Holden', 'Honda', 'Hummer', 'Hyundai',
#                'Infiniti', 'Isuzu', 'Iveco', 'JAC', 'Jaguar', 'Jeep', 'Jinbei', 'Keyton', 'Kia', 'LADA',
#                'Lamborghini',
#                'Lancia', 'Land Rover', 'Landwind', 'LDV', 'LEVC', 'Lexus', 'Lifan', 'Lincoln', 'Lotus', 'Luxgen',
#                'Mahindra', 'MAN', 'Maruti', 'Maserati', 'Maybach', 'Mazda', 'McLaren', 'Mercedes-Benz',
#                'Mercedes-Maybach', 'Mercury', 'MG', 'MINI', 'Mitsubishi', 'Mosler', 'Nio', 'Nissan', 'Oldsmobile',
#                'Opel', 'Panoz', 'Perodua', 'Peugeot', 'Plymouth', 'Polaris', 'Polestar', 'Pontiac', 'Porsche',
#                'Proton',
#                'Qiantu', 'Ram', 'Ravon', 'Renault', 'Renault Samsung', 'Roewe', 'Rolls-Royce', 'Rover', 'Saab',
#                'Saturn', 'Scion', 'Seat', 'Seres', 'Skoda', 'Smart', 'SsangYong', 'Subaru', 'Suzuki', 'Tata',
#                'Tesla',
#                'Toyota', 'UAZ', 'Vauxhall', 'VAZ', 'Venucia', 'Volkswagen', 'Volvo', 'Wuling', 'Zedriv']


brands_dict = get_brands()

data_dict = {brand: {'link': link, 'models': {}} for brand, link in brands_dict.items()}
# data_dict = {'Seat': {'link': '/size/seat/', 'models': {}}}

for brand in data_dict:
    try:
        brand_url = data_dict[brand]['link']
        bs = without_driver(SITE_URL + brand_url)
        model_tags_list = bs.find_all('a', {'itemprop': 'itemListElement'})
        if not model_tags_list:
            bs = with_driver(SITE_URL + brand_url)
            model_tags_list = bs.find_all('a', {'itemprop': 'itemListElement'})
        models_list = list(set([m.get_text() for m in model_tags_list]))
        t_temp = []
        models_dict = {}
        for tag in model_tags_list:
            model_name = tag.get_text()
            if model_name not in t_temp:
                models_dict[model_name] = {'link': tag.get('href'), 'years': {}}
                t_temp.append(model_name)
        data_dict[brand]['models'] = models_dict
        for model in models_dict:
            try:
                year_url = models_dict[model]['link']
                bs = without_driver(SITE_URL + year_url)
                year_tags_list = bs.find_all('a', {'itemprop': 'itemListElement'})
                if not year_tags_list:
                    bs = with_driver(SITE_URL + year_url)
                    year_tags_list = bs.find_all('a', {'itemprop': 'itemListElement'})
                t_temp = []
                years_dict = {}
                for tag in year_tags_list:
                    year = tag.get_text()
                    if year not in t_temp:
                        years_dict[year] = {'link': tag.get('href'), 'item_ids': get_id(tag.get('href'))}
                        t_temp.append(year)
                data_dict[brand]['models'][model]['years'] = years_dict
                print(brand, model, years_dict)
            except Exception as e:
                print(e)
                error = f"{brand}_{model}_{e.__str__()}\n"
                with open('log.txt', 'a') as file:
                    file.write(error)
                continue
    except Exception as e:
        print(e)
        error = f"{brand}_{e.__str__()}\n"
        with open('log.txt', 'a') as file:
            file.write(error)
        continue

with open('data_dict.txt', 'w') as file:
    file.write(json.dumps(data_dict))
