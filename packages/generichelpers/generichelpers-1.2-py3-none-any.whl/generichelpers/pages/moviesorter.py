"""Movies sorter page"""

import os
import pandas as pd
import streamlit as st
from io import StringIO
from devs.moviesorter import MoviesSorter
from pages import CSS
from st_pages import add_page_title


class MoviesSorterStAssist(object):
    """streamlit assist class for sorting movie files/folders/listing"""
    def __init__(self):
        add_page_title(layout='wide')
        # st.set_page_config(page_title='Movies Sorter', page_icon=':cinema:')
        st.markdown(CSS, unsafe_allow_html=True)
        st.markdown(
            '''
            <style>
                div[class*="stSelect"]>label>div[data-testid="stMarkdownContainer"]>p {
                    font-size: 13px;
                    color: black;
                }
                .stSubmitButton, div.stButton {
                    text-align:right;
                }
            </style>
            ''', unsafe_allow_html=True
        )
        st.markdown('<h2 class="head-h2">Sort movies files/folders/listings</h2>', unsafe_allow_html=True)
        st.markdown('<p class="para-p1">This app sorts movies files/folders (in year buckets) or listings (by year/IMDB)</p>', unsafe_allow_html=True)
        self.movie_sorter = MoviesSorter()  # call the movies sorter class

    def sort_movie_folders_st(self):
        """Sort movie files/folders"""
        st.write("**Provide inputs for movie files/folders sorting👇**")
        input_data = pd.DataFrame(
            [
                {
                    "param": "start_year",
                    "description": "Start year of folder buckets ('int' value)",
                    "value": 1950
                },
                {
                    "param": "year_interval",
                    "description": "The year buckets interval ('int' value)",
                    "value": 10
                }
            ]
        )
        input_data = input_data.style.set_properties(**{'background-color': 'LightCyan'}, subset=['param'])
        edited_data = st.data_editor(input_data, hide_index=True, disabled=('param', 'description'))
        base_path = st.text_input('**Provide the base folder path :file_folder:**')
        if st.button('Submit'):
            start_year, year_interval = edited_data['value']
            self.movie_sorter.sort_movie_folders(base_path, start_year, year_interval)
            response = self.movie_sorter.movement_status
            st.write(response)

    def sort_movie_listing_st(self):
        """Sort movie listings"""
        # base_path = st.text_input('**Provide the path of the movies list to sort :spiral_note_pad:**')
        upload_file = st.file_uploader('**Provide the `.txt` file for movies list to sort :spiral_note_pad:**', type=(['.txt']))
        if upload_file:
            str_io = StringIO(upload_file.getvalue().decode('utf-8'))
            movies_list = str_io.read()
        sort_by = st.selectbox(label='**Choose the sort option👇**', options=('imdb', 'year'))
        if st.button('Submit'):
            self.movie_sorter.sort_movie_listing(movies_list, sort_by, False)
            download_name = f'{os.path.splitext(os.path.basename(upload_file.name))[0]}_sorted.txt'
            st.download_button(
                'Download sorted movies list',
                self.movie_sorter.sorted_movies,
                file_name=download_name,
                type='primary'
            )
            st.write(f'**{self.movie_sorter.movement_status}**')

    def main_executor(self):
        """The main module that performs all tasks and displays to page"""
        selected_op = st.radio(
            label='Select the desired movie sort operation to perform',
            options=('Sort movie files/folders', 'Sort movie lists'),
            index=None
        )
        if selected_op == 'Sort movie files/folders':
            self.sort_movie_folders_st()
        elif selected_op == 'Sort movie lists':
            self.sort_movie_listing_st()


# +++++++++++++++++
# The main streamlit operations for this page
if __name__ == "__main__":
    MoviesSorterStAssist().main_executor()
