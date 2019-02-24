from urllib import request
from lxml import html
from peewee import *
import uuid

db = PostgresqlDatabase('Articles', user='postgres', password='postgres', host='localhost', port=5432)


class Students(Model):
    id = UUIDField(primary_key=True)
    name = CharField(max_length=32)
    surname = CharField(max_length=32)
    mygroup = CharField(max_length=6)

    class Meta:
        database = db
        db_table = 'students'


class Article(Model):
    id = UUIDField(primary_key=True)
    title = CharField(max_length=256)
    keywords = CharField(max_length=256)
    content = TextField()
    url = CharField(max_length=128)
    student_id = ForeignKeyField(Students, to_field='id', db_column='student_id')

    class Meta:
        database = db
        db_table = 'articles'


def main():
    student_id = '61b2b3e2-51e2-45f6-8846-c1899dbf13f5'

    urls = ['https://www.igromania.ru/article/30671/Far_Cry_Za_chto_my_lyubim_i_nenavidim_seriyu.html',
            'https://www.igromania.ru/article/30667/Obzor_Crackdown_3_Luchshe_pozdno.html',
            'https://www.igromania.ru/article/30670/CHto_podarit_iemu_i_na_23_fevralya_Pokazhi_iey_i_yetot_tekst.html',
            'https://www.igromania.ru/article/30669/Obzor_Far_Cry_New_Dawn_Kakoy-to_nepravilnyy_postapokalipsis.html',
            'https://www.igromania.ru/article/30668/Pervyy_vzglyad_na_Jump_Force_CHisto_nishevyy_produkt.html',
            'https://www.igromania.ru/article/30665/Obzor_Metro_Exodus_Igra_na_kontrastah.html',
            'https://www.igromania.ru/article/30664/Prevyu_Save_Koch_Kryostnyy_svin_i_razumnaya_plesen.html',
            'https://www.igromania.ru/article/30658/Alita_Boevoy_angel-Rodriges_vernulsya.html',
            'https://www.igromania.ru/article/30663/Civilization_VI_Gathering_Storm_Burya_vostorga.html',
            'https://www.igromania.ru/article/30662/Kogo_dobavit_v_Mortal_Kombat_11_krome_SHyeggi.html',
            'https://www.igromania.ru/article/30660/Pochemu_Apex_Legends_rabotaet_Sdelali_kak_dlya_sebya.html',
            'https://www.igromania.ru/article/30659/Obzor_Re-Legion_Protivopolozhnosti_ne_prityagivayutsya.html',
            'https://www.igromania.ru/article/30656/Vo_chto_my_igrali_5_10_15_i_20_let_nazad.html',
            'https://www.igromania.ru/article/30655/LEGO_Film_2_Bezumnyy_Maks_protiv_glamura.html',
            'https://www.igromania.ru/article/30653/Desyat_drakonov_dlya_Deyeneris_Kto_mog_by_zamenit_Drogona_Reyegalya_i_Vizeriona.html',
            'https://www.igromania.ru/article/30651/Pervyy_vzglyad_na_Kingdom_Hearts_III_Kak_igraetsya_novichku.html',
            'https://www.igromania.ru/article/30652/Prevyu_The_Division_2_Kooperativnyy_shuter_dlya_vseh.html',
            'https://www.igromania.ru/article/30649/Vsyo_chto_my_znaem_o_PlayStation_5.html',
            'https://www.igromania.ru/article/30647/Prevyu_Anthem_Zheleznyy_chelovek_protiv_Avatara.html',
            'https://www.igromania.ru/article/30621/Obzor_Dragon_Quest_XI_Echoes_of_an_Elusive_Age_Odin_vzglyad_nazad.html',
            'https://www.igromania.ru/article/30645/Prevyu_Rage_2_Dzhabba_Hatt_Pandora_Bulletstorm.html',
            'https://www.igromania.ru/article/30646/Luchshie_i_hudshie_chasti_Resident_Evil_Vzlyoty_i_padeniya_legendarnoy_serii.html',
            'https://www.igromania.ru/article/30643/Multipleer_Ace_Combat_7_Skies_Unknown_Ne_vse_my_idealny.html',
            'https://www.igromania.ru/article/30626/Super_Smash_Bros_Ultimate_Draka_yepicheskih_masshtabov.html',
            'https://www.igromania.ru/article/30638/Remeyk_Resident_Evil_2_Bolshoy_perepoloh_v_malenkom_Rakkun-siti.html',
            'https://www.igromania.ru/article/30629/Ace_Combat_7_Skies_Unknown_Legendy_ne_umirayut.html',
            'https://www.igromania.ru/article/30617/Achtung_Cthulhu_Tactics_Ni_Ktulhu_ni_taktiki.html',
            'https://www.igromania.ru/article/30568/The_Bards_Tale_Barrows_Deep_Bard_ne_umer_on_prosto_tak_pahnet.html',
            'https://www.igromania.ru/article/30590/Just_Cause_4_Dayosh_revolyuciyu.html',
            'https://www.igromania.ru/article/30587/Obzor_Sony_PlayStation_Classic_Neodnoznachnaya_klassika.html'
            ]

    Students.create_table()
    Article.create_table()

    sid = uuid.uuid4()
    student = Students(id=sid, name='Дамир', surname='Серазетдинов', mygroup='11-501')
    student.save(force_insert=True)

    for url in urls:
        with request.urlopen(url) as response:
            text = response.read().decode('utf-8')
            tree = html.fromstring(text)

        title = tree.xpath('//h1[@class="page_article_ttl haveselect"]')[0].text_content()

        keywords = tree.xpath('//a[@class="go_link t_gray"]')[0].text_content()

        content = tree.xpath('//div[@class="universal_content clearfix"]/div')
        content = ''.join(elem.text_content() for elem in content)

        article = Article(id=uuid.uuid4(), title=title, keywords=keywords, content=content, url=url, student_id=sid)
        article.save(force_insert=True)


if __name__ == '__main__':
    main()
