from .db import connect
from psycopg2.extras import RealDictCursor

phone_insert_sql = '''
insert into phone (
    internal_memory, 
    ram, 
    model,
    brand_id,
    release,
    height,
    width, 
    thickness, 
    resolution, 
    ppi, 
    cpu_id, 
    chipset_id, 
    gpu_id, 
    memory_card_dedicated, 
    wifi, 
    sim, 
    connector, 
    audio_jack, 
    bluetooth_version, 
    gps, 
    nfc, 
    radio, 
    battery_capacity, 
    battery_removable, 
    image_url)
    values (ARRAY[%s], ARRAY[%s], %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
'''


def addPhone(phone_data: dict) -> None:
    conn = connect()
    with conn.cursor(cursor_factory=RealDictCursor) as crsr:
        p = phone_data
        if p['brand_name'] != "":
            crsr.execute('insert into brand (name) values (%s) on conflict do nothing;', (p['brand_name'],))
        if p['cpu_name'] != "":
            crsr.execute('insert into cpu (name) values (%s) on conflict do nothing;', (p['cpu_name'],))
        if p['chipset_name'] != "":
            crsr.execute('insert into chipset (name) values (%s) on conflict do nothing;', (p['chipset_name'],))
        if p['gpu_name'] != "":
            crsr.execute('insert into gpu (name) values (%s) on conflict do nothing;', (p['gpu_name'],))

        crsr.execute('''
        select 
            brand_id, brand.name as brand_name, 
            cpu_id, cpu.name as cpu_name,
            chipset_id, chipset.name as chipset_name, 
            gpu_id, gpu.name  as gpu_name
        from brand, cpu, chipset, gpu
        where brand.name = %s
            and cpu.name = %s
            and chipset.name = %s
            and gpu.name = %s;
        ''', (p['brand_name'], p['cpu_name'], p['chipset_name'], p['gpu_name']))
        phone_db = crsr.fetchone()
        crsr.execute(phone_insert_sql, (
            phone_data['internal_memory'] or 0,
            phone_data['ram'] or 0,
            phone_data['model'],
            phone_db['brand_id'],
            phone_data['release'],
            phone_data['height'],
            phone_data['width'],
            phone_data['thickness'],
            phone_data['resolution'],
            phone_data['ppi'],
            phone_db['cpu_id'],
            phone_db['chipset_id'],
            phone_db['gpu_id'],
            True if phone_data['memory_card_dedicated'] == 'y' else False,
            phone_data['wifi'],
            phone_data['sim'],
            phone_data['connector'],
            True if phone_data['audio_jack'] else False,
            phone_data['bluetooth_version'],
            True if phone_data['gps'] else False,
            True if phone_data['nfc'] else False,
            True if phone_data['radio'] == 'y' else False,
            phone_data['battery_capacity'],
            True if phone_data['battery_removable'] == 'y' else False,
            phone_data['photourl']
        )
                     )
        conn.commit()


def deletePhone(phone_data: dict) -> None:
    conn = connect()
    with conn.cursor() as crsr:
        crsr.execute('''
        delete from phone 
            where model = %s
            and brand_id = (select brand_id from brand where brand.name = %s) 
        ''', (phone_data['model'], phone_data['brand_name']))
        conn.commit()


def updatePhone(phone_data: dict, cameralist: list) -> None:
    # return edited data
    conn = connect()
    phone_data.pop('cameras')
    with conn.cursor() as crsr:
        # phone_data update
        crsr.execute('select phone_id from phone p where p.model = %(model)s', phone_data)
        phone_id = crsr.fetchone()[0]
        if phone_id:
            phone_update_set_clauses = ["{} = '{}'".format(k, v) for k, v in phone_data.items()]
            query = "update {} set {} where {} = {}".format("phone", ','.join(phone_update_set_clauses), "phone_id",
                                                            phone_id)
            print(query)
            crsr.execute(query)

            # camera_data update
            crsr.execute('delete from "phone-camera" pc where phone_id = %s', (phone_id,))
            print(cameralist)
            for c in cameralist:
                crsr.execute('insert into camera (mp, f) values (%s, %s) on conflict do nothing;', (c['mp'], c['f']))
                # crsr.execute("select camera_id from camera where camera.mp = %s and camera.f = %s", (c['mp'], str(c['f'])))
                crsr.execute(
                    '''
                    insert into "phone-camera" (phone_id, camera_id) 
                    values (%s, (select camera_id from camera where camera.mp = %s and camera.f = %s))
                    on conflict do nothing;
                    ''', (phone_id, c['mp'], str(c['f'])))
                conn.commit()

