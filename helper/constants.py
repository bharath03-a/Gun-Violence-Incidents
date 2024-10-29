# Snowflake credentials
# PASTE THE SF CREDS HERE

SF_WAREHOUSE = "mis584_gva_dw"
SF_DATABASE = "gva_database"
SF_SCHEMA = "gva_schema"
SF_TABLE_NAME = "gva_cleaned_data"
SF_TABLE_SCHEMA = "(incident_id INTEGER, date DATE, state STRING, city_or_county STRING, address STRING, n_killed INTEGER, n_injured INTEGER, \
    congressional_district INTEGER, incident_characteristics STRING, latitude DOUBLE, longitude DOUBLE, n_guns_involved INTEGER, notes STRING, \
        year INTEGER, month INTEGER, day_of_week INTEGER, gun_stolen_not_stolen_freq INTEGER, gun_stolen_stolen_freq INTEGER, gun_stolen_unknown_freq INTEGER, \
            gun_type_ak_freq INTEGER, gun_type_auto_freq INTEGER, gun_type_gauge_freq INTEGER, gun_type_handgun_freq INTEGER, gun_type_lr_freq INTEGER, gun_type_mag_freq INTEGER, \
                gun_type_mm_freq INTEGER, gun_type_rem_ar_freq INTEGER, gun_type_rifle_freq INTEGER, gun_type_shotgun_freq INTEGER, gun_type_spl_freq INTEGER, gun_type_spr_freq INTEGER, \
                    gun_type_sw_freq INTEGER, gun_type_unknown_freq INTEGER, gun_type_win_freq INTEGER, participant_age_group_adult_18plus_freq INTEGER, participant_age_group_child_0_11_freq INTEGER, \
                        participant_age_group_teen_12_17_freq INTEGER, participant_gender_female_freq INTEGER, participant_gender_male_freq INTEGER, participant_status_arrested_freq INTEGER, participant_status_injured_freq INTEGER, \
                            participant_status_killed_freq INTEGER, participant_status_unharmed_freq INTEGER, participant_type_subject_suspect_freq INTEGER, participant_type_victim_freq INTEGER)"


CLEANED_DATA_PATH = "data/gun_violence_cleaned_data_2013_2018.csv"