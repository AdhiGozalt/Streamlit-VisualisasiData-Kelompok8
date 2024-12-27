import streamlit as st 
import pandas as pd
import plotly.express as px 
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from datetime import datetime
from streamlit_lottie import st_lottie
import requests
import json

st.set_page_config(page_title="2024 Paris Olympics Dashboard",page_icon="🏅",layout="wide")

selected = option_menu(
    menu_title="Main Menu",
    options=["About Paris Olympics 2024","Athletes Data", "Disciplines", "Medals Data", "Schedule Data"],
    icons=["paper","people", "basket", "trophy", "calendar"],
    menu_icon="cast",
    default_index=0,
    orientation="vertical",
)

file = "dataset/athletes.csv"
df = pd.read_csv(file)

st.sidebar.image("pic/parislogo.jpg", caption= "https://www.kaggle.com/datasets/piterfm/paris-2024-olympic-summer-games/data?select=athletes.csv")
st.sidebar.write("Muhammad Adhi Gozalt : 1301213212")
st.sidebar.write("Naufal Alfarisi : 1301213452")
st.sidebar.write("Azzam Abdurrahman : 1301184295")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

if selected == "About Paris Olympics 2024":
    st.subheader("Tentang Olimpiade Paris 2024")
    lottie_animation = load_lottiefile("./olympicLottie.json")  
    st_lottie(
        lottie_animation,
        speed=1,
        reverse=False,
        loop=True,
        quality="high",  
        height=300,
        width=300,
        key="paris_olympics",
    )
    
   
    
    st.markdown("""
        <div style="text-align: justify;">
                
            Olimpiade Paris 2024 adalah edisi ke-33 dari Olimpiade Musim Panas, yang akan berlangsung di Paris, Prancis, dari tanggal 26 Juli hingga 11 Agustus 2024.  
            Acara ini akan menjadi yang ketiga kalinya Paris menjadi tuan rumah Olimpiade setelah sebelumnya diadakan pada tahun 1900 dan 1924.  
            Paris 2024 mengusung tema keberlanjutan dengan memanfaatkan infrastruktur yang sudah ada dan menggunakan energi terbarukan.  
            Dengan 32 cabang olahraga dan lebih dari 11.000 atlet dari seluruh dunia, Olimpiade ini akan menjadi perayaan olahraga, budaya, dan persatuan global.  
            Selain itu, Olimpiade Paris 2024 juga mencetak sejarah dengan memasukkan cabang olahraga baru seperti breakdancing untuk pertama kalinya dalam sejarah Olimpiade.
        </div>
    """, unsafe_allow_html=True)
    
  
    st.subheader("Galeri Foto Olimpiade Paris 2024")
    
 
    image_urls = [
        "https://img.olympics.com/images/image/private/t_16-9_1920/f_auto/v1538355600/primary/bqkeqmlhf0mytsetfabh", 
        "https://c.ndtvimg.com/2024-08/eroggbio_yusuf-dikec_625x300_24_August_24.jpeg?im=FeatureCrop,algorithm=dnn,width=806,height=605",  
        "https://akns-images.eonline.com/eol_images/Entire_Site/2024712/rs_1024x759-240812065032-raygun1.jpg?fit=around%7C1024:759&output-quality=90&crop=1024:759;center,top",  
        "https://setkab.go.id/wp-content/uploads/2024/08/WhatsApp-Image-2024-08-09-at-5.42.04-AM.jpeg"
    ]
    
    cols = st.columns(len(image_urls))
    for i, url in enumerate(image_urls):
        with cols[i]:
            st.image(url, use_container_width=True, caption=f"Foto {i+1}")



if selected == "Athletes Data":
    file_athletes = "dataset/athletes.csv"
    df_athletes = pd.read_csv(file_athletes)
    st.subheader("Data Atlit")
    
    columns_to_drop = ["current", "name_tv", "function", "age", "height", "weight", 
                       "hero", "family", "reason", "influence", "sporting_relatives", 
                       "ritual", "other_sports"]
    df_cleaned = df.drop(columns=columns_to_drop, errors="ignore")
    
    st.sidebar.header("Filter Athletes Data")
    gender = st.sidebar.multiselect(
        "Select Gender",
        options=df_cleaned["gender"].unique(),
        default=df_cleaned["gender"].unique(),
    )

    disciplines = st.sidebar.multiselect(
        "Select Disciplines",
        options=df_cleaned["disciplines"].unique(),
        default=df_cleaned["disciplines"].unique(),
    )

    filtered_data = df_cleaned[
        (df_cleaned["gender"].isin(gender)) & 
        (df_cleaned["disciplines"].isin(disciplines))
    ]
    st.write("Filtered Data:")
    st.dataframe(filtered_data)

    st.subheader("Distribusi Gender")
    gender_count = df_cleaned['gender'].value_counts().reset_index()
    gender_count.columns = ['Gender', 'Count']
    fig_horizontal_bar = px.bar(
        gender_count,
        x="Count",
        y="Gender",
        orientation="h",
        title="Distribusi Gender menggunakan Horizontal Bar Chart",
        color="Gender",
        color_discrete_map={"Female": "lightpink", "Male": "lightblue"},
        text="Count"
    )
    fig_horizontal_bar.update_layout(
        xaxis_title="Count",
        yaxis_title="Gender",
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_horizontal_bar)

    df_cleaned['birth_date'] = pd.to_datetime(df_cleaned['birth_date'], errors='coerce')
    current_date = datetime.now()
    df_cleaned['age'] = df_cleaned['birth_date'].apply(
        lambda x: current_date.year - x.year if pd.notnull(x) else None
    )
    age_groups = ['Under 20', '21-30', '31-40', '41-50', '51+']
    df_cleaned['age_group'] = pd.cut(
        df_cleaned['age'],
        bins=[0, 20, 30, 40, 50, 100],
        labels=age_groups,
        right=False
    )
    age_group_count = df_cleaned['age_group'].value_counts().reset_index()
    age_group_count.columns = ['Age Group', 'Count']
    st.subheader("Distribusi Usia Atlit")
    fig_pie = px.pie(
        age_group_count,
        names="Age Group",
        values="Count",
        title="Distribusi Usia dalam grup menggunakan Pie Chart",
        hole=0.4,
        color="Age Group",
        color_discrete_map={
            "Under 20": "green",
            "21-30": "lightgreen",
            "31-40": "gold",
            "41-50": "brown",
            "51+": "red"
        }
    )
    st.plotly_chart(fig_pie)

    file_path = "dataset/coaches.csv"
    df_coaches = pd.read_csv(file_path)

    st.subheader("Data Pelatih")
    st.write(df_coaches)

    country_counts = df_coaches['country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Number of Coaches']

    st.subheader("Jumlah pelatih pada setiap negara")
    st.bar_chart(data=country_counts, x='Country', y='Number of Coaches')

if selected == "Disciplines":
    file_path = "dataset/coaches.csv"
    df_coaches = pd.read_csv(file_path)

    discipline_counts = df_coaches['disciplines'].value_counts().reset_index()
    discipline_counts.columns = ['Discipline', 'Count']

    fig_pie_disciplines = px.pie(
        discipline_counts,
        names="Discipline",
        values="Count",
        title="Distribusi Cabang Olahraga menggunakan Pie Chart",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    st.subheader("Distribusi Cabang Olahraga")
    st.plotly_chart(fig_pie_disciplines)

if selected == "Medals Data":
    file_medalists = "dataset/medallists.csv"
    df_medallists = pd.read_csv(file_medalists)
    st.subheader("Data Para Medalis")

    columns_to_drop = [
        "medal_date", "country_code", "nationality_code", "nationality",
        "nationality_long", "team", "team_gender", "event_type", "url_event",
        "birth_date", "code_team", "is_medallist"
    ]
    df_cleaned = df_medallists.drop(columns=columns_to_drop, errors="ignore")

    st.sidebar.header("Filter Medallists Data")

    discipline = st.sidebar.multiselect(
        "Select Discipline",
        options=df_cleaned["discipline"].unique(),
        default=df_cleaned["discipline"].unique()
    )

    gender = st.sidebar.multiselect(
        "Select Gender",
        options=df_cleaned["gender"].unique(),
        default=df_cleaned["gender"].unique()
    )

    medal_type = st.sidebar.multiselect(
        "Select Medal Type",
        options=df_cleaned["medal_type"].unique(),
        default=df_cleaned["medal_type"].unique()
    )

    filtered_data = df_cleaned[
        (df_cleaned["discipline"].isin(discipline)) & 
        (df_cleaned["gender"].isin(gender)) & 
        (df_cleaned["medal_type"].isin(medal_type))
    ]

    st.write("Filtered Medallists Data:")
    st.dataframe(filtered_data)

    st.subheader("Distribusi Medal (Gold, Silver, Bronze)")
    medal_counts = filtered_data["medal_type"].value_counts().reset_index()
    medal_counts.columns = ["Medal Type", "Count"]
    
    fig_pie = px.pie(
        medal_counts,
        names="Medal Type",
        values="Count",
        title="Distribution Medal (Gold, Silver, Bronze)",
        hole=0.4,
        color="Medal Type",
        color_discrete_map={
            "Gold Medal": "#FFD700",
            "Silver Medal": "silver",
            "Bronze Medal": "#CD7F32"
        }
    )
    st.plotly_chart(fig_pie)
   
    medal_mapping = {0: "All Types", 1: "Gold", 2: "Silver", 3: "Bronze"}

    selected_medal_code = st.sidebar.selectbox(
        "Select Medal Type",
        options=list(medal_mapping.keys()),
        format_func=lambda x: medal_mapping[x]
    )

    if selected_medal_code != 0:
        filtered_medal_data = filtered_data[filtered_data["medal_code"] == selected_medal_code]
        medal_name = medal_mapping[selected_medal_code]
    else:
        filtered_medal_data = filtered_data
        medal_name = "All Types"

    st.subheader(f"Negara dengan medali {medal_name} ")

    if not filtered_medal_data.empty:
        country_medals = (
            filtered_medal_data["country"]
            .value_counts()
            .reset_index()
        )
        country_medals.columns = ["Country", f"{medal_name} Medals"]

        fig_line = px.line(
            country_medals,
            x="Country",
            y=f"{medal_name} Medals",
            
            markers=True,
            line_shape="linear"
        )
        color_map = {
            1: "#FFD700",
            2: "#C0C0C0",
            3: "#CD7F32"
        }

        if selected_medal_code != 0:
            fig_line.update_traces(line_color=color_map[selected_medal_code])
        else:
            fig_line.update_traces(line_color=None)

        fig_line.update_layout(
            xaxis={'categoryorder': 'total ascending'}
        )

        st.plotly_chart(fig_line)
    else:
        st.warning(f"No data available for {medal_name} Medals.")

if selected == "Schedule Data":
    path_data = "dataset/schedules.csv"

    data = pd.read_csv(path_data)

   
    data['start_date'] = pd.to_datetime(data['start_date'])
    data['end_date'] = pd.to_datetime(data['end_date'])
    data.rename(columns={
        'start_date': 'Tanggal Mulai',
        'end_date': 'Tanggal Selesai',
        'day': 'Day',
        'status': 'Status',
        'discipline': 'Cabang Olahraga',
        'discipline_code': 'Kode Cabang',
        'event': 'Acara',
        'event_medal': 'Medal Acara',
        'phase': 'Fase',
        'gender': 'Jenis Kelamin',
        'event_type': 'Tipe Acara',
        'venue': 'Lokasi',
        'venue_code': 'Kode Lokasi',
        'location_description': 'Deskripsi Lokasi',
        'location_code': 'Kode Lokasi Deskripsi',
        'url': 'URL'
    }, inplace=True)

   
    st.sidebar.header("Filter")

   
    cabang_olahraga = data['Cabang Olahraga'].unique()
    pilih_semua_opsi = st.sidebar.checkbox("Pilih Semua Cabang Olahraga", value=True)
    cabang_terpilih = st.sidebar.multiselect(
        "Pilih Cabang Olahraga:", options=cabang_olahraga, default=cabang_olahraga if pilih_semua_opsi else []
    )

    status_terpilih = st.sidebar.multiselect(
        "Pilih Status:", options=data['Status'].unique(), default=data['Status'].unique()
    )

 
    tanggal_terpilih = st.sidebar.date_input(
        "Pilih Rentang Tanggal:", 
        value=[data['Tanggal Mulai'].min().date(), data['Tanggal Mulai'].max().date()], 
        min_value=data['Tanggal Mulai'].min().date(), 
        max_value=data['Tanggal Mulai'].max().date()
    )

  
    data_terfilter = data[
        (data['Cabang Olahraga'].isin(cabang_terpilih)) &
        (data['Status'].isin(status_terpilih)) &
        (data['Tanggal Mulai'].dt.date >= tanggal_terpilih[0]) &
        (data['Tanggal Mulai'].dt.date <= tanggal_terpilih[1])
    ]

    st.write("### Data Terfilter", data_terfilter)

  
    st.write("## Jumlah Acara Berdasarkan Cabang Olahraga")
    jumlah_acara = data_terfilter['Cabang Olahraga'].value_counts().reset_index()
    jumlah_acara.columns = ['Cabang Olahraga', 'Jumlah Acara']
    fig = px.bar(jumlah_acara, x='Jumlah Acara', y='Cabang Olahraga', text='Jumlah Acara',
                title="Jumlah Acara Berdasarkan Cabang Olahraga", labels={'Jumlah Acara': 'Jumlah Acara'})
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig)

   
    st.write("## Timeline Acara")
    linimasa_fig = px.timeline(
        data_terfilter, 
        x_start="Tanggal Mulai", x_end="Tanggal Selesai", y="Cabang Olahraga", color="Status",
        title="Timeline Acara Berdasarkan Cabang Olahraga",
        labels={"Cabang Olahraga": "Cabang Olahraga", "Tanggal Mulai": "Tanggal Mulai", "Tanggal Selesai": "Tanggal Selesai"}
    )
    linimasa_fig.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(linimasa_fig)

  
    st.write("## Acara Berdasarkan Lokasi")
    jumlah_lokasi = data_terfilter['Lokasi'].value_counts().reset_index()
    jumlah_lokasi.columns = ['Lokasi', 'Jumlah Acara']
    lokasi_fig = px.bar(jumlah_lokasi, x='Jumlah Acara', y='Lokasi', text='Jumlah Acara',
                    title="Acara Berdasarkan Lokasi", labels={'Jumlah Acara': 'Jumlah Acara'})
    lokasi_fig.update_traces(textposition='outside')
    lokasi_fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(lokasi_fig)