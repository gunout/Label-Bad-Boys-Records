# dashboard_badboy_records.py
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
from datetime import datetime
import warnings
import base64
import io
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="ANALYSE STRATÉGIQUE - BAD BOY RECORDS",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec thème Bad Boy (noir, blanc, argent)
st.markdown("""
<style>
    .main {
        color: #ffffff !important;
        background-color: #000000 !important;
    }
    
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        border-bottom: 3px solid #C0C0C0;
        padding-bottom: 1rem;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        background: linear-gradient(90deg, #000000, #333333, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .academic-card {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        border: 1px solid #444444;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
        color: #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .academic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(192, 192, 192, 0.3);
        border-color: #C0C0C0;
    }
    
    .puff-card { 
        border-left: 5px solid #FFD700; 
        background: linear-gradient(135deg, #1a1a0a 0%, #2d2d1a 100%);
    }
    .biggie-card { 
        border-left: 5px solid #C0C0C0; 
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    }
    .mase-card { 
        border-left: 5px solid #FF6B6B; 
        background: linear-gradient(135deg, #1a0a0a 0%, #2d1a1a 100%);
    }
    .lilkim-card { 
        border-left: 5px solid #FF69B4; 
        background: linear-gradient(135deg, #1a0a1a 0%, #2d1a2d 100%);
    }
    .faith-card { 
        border-left: 5px solid #9370DB; 
        background: linear-gradient(135deg, #0a1a1a 0%, #1a2d2d 100%);
    }
    .total-card { 
        border-left: 5px solid #4169E1; 
        background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2d 100%);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #C0C0C0 !important;
        margin: 0.5rem 0;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    .section-title {
        color: #ffffff !important;
        border-bottom: 2px solid #C0C0C0;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
        font-size: 1.6rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
    }
    
    .subsection-title {
        color: #ffffff !important;
        border-left: 4px solid #C0C0C0;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .stMarkdown {
        color: #ffffff !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .secondary-text {
        color: #cccccc !important;
    }
    
    .light-text {
        color: #999999 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #0a0a0a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1a1a1a;
        border-radius: 5px;
        color: #ffffff !important;
        font-weight: 500;
        border: 1px solid #444444;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2d2d2d;
        border-color: #C0C0C0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #C0C0C0 !important;
        color: #000000 !important;
        font-weight: 600;
        border-color: #C0C0C0;
    }
    
    .card-content {
        color: #ffffff !important;
    }
    
    .card-secondary {
        color: #cccccc !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%);
        color: #000000;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(192, 192, 192, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFFFFF 0%, #C0C0C0 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.4);
    }
    
    .stDataFrame {
        background-color: #0a0a0a;
        color: #ffffff;
    }
    
    .stSelectbox > div > div {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    .stSlider > div > div > div {
        background-color: #C0C0C0;
    }
    
    /* Style pour les graphiques Plotly */
    .js-plotly-plot .plotly .modebar {
        background-color: rgba(10, 10, 10, 0.8) !important;
    }
    
    .js-plotly-plot .plotly .modebar-btn {
        background-color: transparent !important;
        color: #ffffff !important;
    }
    
    /* Badge Bad Boy */
    .badboy-badge {
        display: inline-block;
        background: #000000;
        color: #C0C0C0;
        padding: 5px 15px;
        border-radius: 20px;
        border: 2px solid #C0C0C0;
        font-weight: bold;
        font-size: 0.9rem;
        margin: 0 5px 10px 0;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #444444;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #555555;
    }
</style>
""", unsafe_allow_html=True)

class BadBoyAnalyzer:
    def __init__(self):
        # Définition de la palette de couleurs pour Bad Boy Records
        self.color_palette = {
            'P. DIDDY': '#FFD700',        # Or
            'THE NOTORIOUS B.I.G.': '#C0C0C0',     # Argent
            'MASE': '#FF6B6B',          # Rouge clair
            'LIL\' KIM': '#FF69B4',     # Rose vif
            'FAITH EVANS': '#9370DB',   # Violet
            'TOTAL': '#4169E1',        # Bleu royal
            '112': '#FF8C00',          # Orange foncé
            'Période Classique': '#C0C0C0',
            'Période Moderne': '#FFD700'
        }
        
        # Couleurs pour les types de données
        self.data_colors = {
            'Ventes': '#C0C0C0',
            'Albums': '#FFD700',
            'Artistes': '#4169E1',
            'Revenus': '#9370DB',
            'Croissance': '#FF6B6B'
        }
        
        self.initialize_data()
        
    def initialize_data(self):
        """Initialise les données complètes sur Bad Boy Records"""
        
        # Données principales sur le label
        self.label_data = {
            'fondation': 1993,
            'fondateur': 'Sean "Puffy" Combs',
            'statut': 'Label indépendant (filiale de Atlantic Records/Warner Music Group)',
            'siege': 'New York City, New York, USA',
            'specialisation': 'Hip-hop, R&B, Pop rap',
            'philosophie': "Luxe, glamour, succès commercial",
            'distribution': 'Arista Records (1993-2001), Atlantic Records (2001-présent)'
        }

        # Données des artistes principaux
        self.artists_data = {
            'P. DIDDY': {
                'debut': 1993,
                'genre': 'Hip-hop, R&B, Pop',
                'albums_badboy': 6,
                'ventes_totales': 25000000,
                'succes_principal': 'No Way Out (1997)',
                'statut': 'Fondateur et CEO',
                'impact': 'Visionnaire commercial, producteur',
                'annees_activite': '1993-présent',
                'albums_principaux': ['No Way Out', 'Forever', 'Press Play'],
                'chiffre_affaires_estime': 150000000,
                'public_cible': 'Mainstream, clubs, luxe',
                'tournees': 'Mondiales'
            },
            'THE NOTORIOUS B.I.G.': {
                'debut': 1994,
                'genre': 'Hip-hop, Rap East Coast',
                'albums_badboy': 2,
                'ventes_totales': 17000000,
                'succes_principal': 'Ready to Die (1994)',
                'statut': 'Artiste légendaire',
                'impact': 'Icône du hip-hop East Coast',
                'annees_activite': '1994-1997',
                'albums_principaux': ['Ready to Die', 'Life After Death'],
                'chiffre_affaires_estime': 100000000,
                'public_cible': 'Hip-hop pur, urbain',
                'tournees': 'Nationales'
            },
            'MASE': {
                'debut': 1997,
                'genre': 'Hip-hop, Pop rap',
                'albums_badboy': 2,
                'ventes_totales': 5000000,
                'succes_principal': 'Harlem World (1997)',
                'statut': 'Artiste à succès',
                'impact': 'Style unique, flow reconnaissable',
                'annees_activite': '1997-1999, 2004-2006',
                'albums_principaux': ['Harlem World', 'Double Up'],
                'chiffre_affaires_estime': 25000000,
                'public_cible': 'Mainstream, jeunes',
                'tournees': 'Nationales'
            },
            'LIL\' KIM': {
                'debut': 1996,
                'genre': 'Hip-hop, Hardcore rap',
                'albums_badboy': 1,
                'ventes_totales': 6000000,
                'succes_principal': 'Hard Core (1996)',
                'statut': 'Queen Bee',
                'impact': 'Pionnière du rap féminin hardcore',
                'annees_activite': '1996-2000',
                'albums_principaux': ['Hard Core', 'The Notorious K.I.M.'],
                'chiffre_affaires_estime': 30000000,
                'public_cible': 'Féminin, urbain, hardcore',
                'tournees': 'Nationales'
            },
            'FAITH EVANS': {
                'debut': 1995,
                'genre': 'R&B, Soul',
                'albums_badboy': 3,
                'ventes_totales': 4000000,
                'succes_principal': 'Faith (1995)',
                'statut': 'First Lady de Bad Boy',
                'impact': 'Voix soul distinctive',
                'annees_activite': '1995-2001',
                'albums_principaux': ['Faith', 'Keep the Faith'],
                'chiffre_affaires_estime': 20000000,
                'public_cible': 'R&B, adult contemporary',
                'tournees': 'Nationales'
            },
            'TOTAL': {
                'debut': 1995,
                'genre': 'R&B, New Jack Swing',
                'albums_badboy': 2,
                'ventes_totales': 3000000,
                'succes_principal': 'Total (1996)',
                'statut': 'Girl group R&B',
                'impact': 'Harmonies R&B années 90',
                'annees_activite': '1995-1999',
                'albums_principaux': ['Total', 'Kima, Keisha, Pam'],
                'chiffre_affaires_estime': 15000000,
                'public_cible': 'R&B, jeunes femmes',
                'tournees': 'Nationales'
            },
            '112': {
                'debut': 1996,
                'genre': 'R&B, Hip-hop soul',
                'albums_badboy': 3,
                'ventes_totales': 8000000,
                'succes_principal': '112 (1996)',
                'statut': 'Boy band R&B',
                'impact': 'Croisement R&B/Hip-hop',
                'annees_activite': '1996-2002',
                'albums_principaux': ['112', 'Room 112', 'Part III'],
                'chiffre_affaires_estime': 40000000,
                'public_cible': 'R&B, jeunes',
                'tournees': 'Nationales'
            }
        }

        # Données chronologiques détaillées
        self.timeline_data = [
            {'annee': 1993, 'evenement': 'Fondation par Sean "Puffy" Combs', 'type': 'Structure', 'importance': 10},
            {'annee': 1994, 'evenement': 'Sortie de Ready to Die (The Notorious B.I.G.)', 'type': 'Album', 'importance': 10},
            {'annee': 1995, 'evenement': 'Signature de Faith Evans', 'type': 'Artiste', 'importance': 8},
            {'annee': 1996, 'evenement': 'Sortie de Hard Core (Lil\' Kim)', 'type': 'Album', 'importance': 9},
            {'annee': 1997, 'evenement': 'Sortie de No Way Out (Puff Daddy)', 'type': 'Album', 'importance': 10},
            {'annee': 1997, 'evenement': 'Assassinat de The Notorious B.I.G.', 'type': 'Événement', 'importance': 10},
            {'annee': 1997, 'evenement': 'Sortie de Harlem World (Mase)', 'type': 'Album', 'importance': 9},
            {'annee': 1998, 'evenement': 'Signature exclusive avec Arista Records', 'type': 'Business', 'importance': 8},
            {'annee': 2001, 'evenement': 'Passe à Atlantic Records', 'type': 'Business', 'importance': 7},
            {'annee': 2002, 'evenement': 'Lancement de la ligne de vêtements Sean John', 'type': 'Diversification', 'importance': 8},
            {'annee': 2005, 'evenement': 'Réapparition de Mase', 'type': 'Artiste', 'importance': 6},
            {'annee': 2015, 'evenement': 'Documentaire "The Bad Boy Family Reunion"', 'type': 'Média', 'importance': 7}
        ]

        # Données financières et commerciales
        self.financial_data = {
            'P. DIDDY': {
                'ventes_albums': 25000000,
                'chiffre_affaires': 150000000,
                'rentabilite': 85,
                'cout_production_moyen': 800000,
                'budget_marketing_moyen': 5000000,
                'roi': 900
            },
            'THE NOTORIOUS B.I.G.': {
                'ventes_albums': 17000000,
                'chiffre_affaires': 100000000,
                'rentabilite': 90,
                'cout_production_moyen': 600000,
                'budget_marketing_moyen': 3000000,
                'roi': 1100
            },
            'MASE': {
                'ventes_albums': 5000000,
                'chiffre_affaires': 25000000,
                'rentabilite': 80,
                'cout_production_moyen': 300000,
                'budget_marketing_moyen': 2000000,
                'roi': 600
            },
            'LIL\' KIM': {
                'ventes_albums': 6000000,
                'chiffre_affaires': 30000000,
                'rentabilite': 75,
                'cout_production_moyen': 250000,
                'budget_marketing_moyen': 1500000,
                'roi': 500
            },
            'FAITH EVANS': {
                'ventes_albums': 4000000,
                'chiffre_affaires': 20000000,
                'rentabilite': 70,
                'cout_production_moyen': 200000,
                'budget_marketing_moyen': 1000000,
                'roi': 400
            },
            'TOTAL': {
                'ventes_albums': 3000000,
                'chiffre_affaires': 15000000,
                'rentabilite': 65,
                'cout_production_moyen': 150000,
                'budget_marketing_moyen': 800000,
                'roi': 300
            },
            '112': {
                'ventes_albums': 8000000,
                'chiffre_affaires': 40000000,
                'rentabilite': 78,
                'cout_production_moyen': 350000,
                'budget_marketing_moyen': 1800000,
                'roi': 550
            }
        }

        # Données de stratégie marketing
        self.marketing_data = {
            'P. DIDDY': {
                'strategie': 'Luxe, glamour, lifestyle de star',
                'cibles': 'Mainstream, clubs, luxe',
                'canaux': ['MTV', 'Radio pop', 'Événements VIP', 'Mode'],
                'budget_ratio': 30,
                'succes': 'Exceptionnel',
                'innovations': 'Marketing de lifestyle'
            },
            'THE NOTORIOUS B.I.G.': {
                'strategie': 'Authenticité East Coast, street cred',
                'cibles': 'Hip-hop pur, urbain',
                'canaux': ['Mixtapes', 'Radio urbaine', 'Presse hip-hop'],
                'budget_ratio': 25,
                'succes': 'Légendaire',
                'innovations': 'Narrative storytelling'
            },
            'MASE': {
                'strategie': 'Image accessible, style distinctif',
                'cibles': 'Jeunes, mainstream',
                'canaux': ['Radio pop', 'Vidéos musicales', 'Apparences publiques'],
                'budget_ratio': 20,
                'succes': 'Très bon',
                'innovations': 'Marketing de personnalité'
            },
            'LIL\' KIM': {
                'strategie': 'Féminisme provocateur, sexualité assumée',
                'cibles': 'Femmes urbaines, LGBTQ+',
                'canaux': ['Magazines mode', 'Radio urbaine', 'Controverses'],
                'budget_ratio': 22,
                'succes': 'Très bon',
                'innovations': 'Marketing féminin hardcore'
            },
            'FAITH EVANS': {
                'strategie': 'Élégance R&B, voix soul',
                'cibles': 'Adultes, R&B traditionnel',
                'canaux': ['Radio adult contemporary', 'TV spéciales', 'Duos'],
                'budget_ratio': 18,
                'succes': 'Bon',
                'innovations': 'Marketing crossover'
            },
            'TOTAL': {
                'strategie': 'Harmonies vocales, glamour années 90',
                'cibles': 'Jeunes femmes, R&B',
                'canaux': ['Radio R&B', 'Vidéos stylisées', 'Concerts'],
                'budget_ratio': 16,
                'succes': 'Modéré',
                'innovations': 'Marketing de groupe'
            },
            '112': {
                'strategie': 'Romantique R&B, harmonies masculines',
                'cibles': 'Jeunes, R&B contemporain',
                'canaux': ['Radio R&B', 'MTV', 'Tournées'],
                'budget_ratio': 20,
                'succes': 'Bon',
                'innovations': 'Marketing de boy band R&B'
            }
        }

        # Données de production
        self.production_data = {
            'P. DIDDY': {
                'albums_produits': 6,
                'duree_contrat': 30,
                'rythme_sorties': '5 ans',
                'qualite_production': 9,
                'autonomie_artistique': 10,
                'support_label': 10
            },
            'THE NOTORIOUS B.I.G.': {
                'albums_produits': 2,
                'duree_contrat': 3,
                'rythme_sorties': '1.5 ans',
                'qualite_production': 10,
                'autonomie_artistique': 9,
                'support_label': 9
            },
            'MASE': {
                'albums_produits': 2,
                'duree_contrat': 8,
                'rythme_sorties': '4 ans',
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 8
            },
            'LIL\' KIM': {
                'albums_produits': 1,
                'duree_contrat': 4,
                'rythme_sorties': '4 ans',
                'qualite_production': 8,
                'autonomie_artistique': 8,
                'support_label': 8
            },
            'FAITH EVANS': {
                'albums_produits': 3,
                'duree_contrat': 6,
                'rythme_sorties': '2 ans',
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 7
            },
            'TOTAL': {
                'albums_produits': 2,
                'duree_contrat': 4,
                'rythme_sorties': '2 ans',
                'qualite_production': 7,
                'autonomie_artistique': 6,
                'support_label': 7
            },
            '112': {
                'albums_produits': 3,
                'duree_contrat': 6,
                'rythme_sorties': '2 ans',
                'qualite_production': 8,
                'autonomie_artistique': 7,
                'support_label': 8
            }
        }

        # Données de gestion et management
        self.management_data = {
            'structure': {
                'type': 'Label indépendant avec backing major',
                'effectif': 40,
                'departements': ['A&R', 'Production', 'Marketing', 'Commercial', 'Legal', 'Mode'],
                'processus_decision': 'Centralisé (P. Diddy)',
                'culture_entreprise': 'Luxe, famille, ambition commerciale'
            },
            'ressources_humaines': {
                'turnover': 'Moyen',
                'expertise': 'Marketing, branding',
                'reseautage': 'Industrie du luxe, médias',
                'formation': 'Professionnelle'
            },
            'finances': {
                'model_economique': 'Branding multiplateforme, licensing',
                'marge_nette': '25-30%',
                'investissement_artistes': 'Long terme, développement',
                'risque': 'Modéré à élevé'
            },
            'relations_artistes': {
                'approche': 'Familiale, protectrice',
                'contrats': 'Standards de l\'industrie',
                'communication': 'Directe, personnelle',
                'loyaute': 'Forte (Bad Boy Family)'
            }
        }

    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">👑 BAD BOY RECORDS - DASHBOARD STRATÉGIQUE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #cccccc; font-size: 1.2rem; margin-bottom: 2rem;">Label de hip-hop américain - Analyse complète 1993-2024</p>', unsafe_allow_html=True)
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_ventes = sum(self.financial_data[artist]['ventes_albums'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card puff-card">
                <div style="color: {self.color_palette['P. DIDDY']}; font-size: 1rem; font-weight: 600; text-align: center;">📀 VENTES TOTALES</div>
                <div class="metric-value" style="color: {self.color_palette['P. DIDDY']}; text-align: center;">{total_ventes:,}</div>
                <div style="color: #cccccc; text-align: center;">Albums vendus</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_artistes = len(self.artists_data)
            st.markdown(f"""
            <div class="academic-card biggie-card">
                <div style="color: {self.color_palette['THE NOTORIOUS B.I.G.']}; font-size: 1rem; font-weight: 600; text-align: center;">🎤 ARTISTES</div>
                <div class="metric-value" style="color: {self.color_palette['THE NOTORIOUS B.I.G.']}; text-align: center;">{total_artistes}</div>
                <div style="color: #cccccc; text-align: center;">Artistes principaux</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_albums = sum(self.artists_data[artist]['albums_badboy'] for artist in self.artists_data)
            st.markdown(f"""
            <div class="academic-card mase-card">
                <div style="color: {self.color_palette['MASE']}; font-size: 1rem; font-weight: 600; text-align: center;">💿 ALBUMS</div>
                <div class="metric-value" style="color: {self.color_palette['MASE']}; text-align: center;">{total_albums}</div>
                <div style="color: #cccccc; text-align: center;">Produits par le label</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            chiffre_affaires_total = sum(self.financial_data[artist]['chiffre_affaires'] for artist in self.financial_data)
            st.markdown(f"""
            <div class="academic-card lilkim-card">
                <div style="color: {self.color_palette['LIL\' KIM']}; font-size: 1rem; font-weight: 600; text-align: center;">💰 CHIFFRE D'AFFAIRES</div>
                <div class="metric-value" style="color: {self.color_palette['LIL\' KIM']}; text-align: center;">{chiffre_affaires_total/1000000:.1f}M$</div>
                <div style="color: #cccccc; text-align: center;">Estimé sur la période</div>
            </div>
            """, unsafe_allow_html=True)

    def create_artist_analysis(self):
        """Analyse complète des artistes"""
        st.markdown('<h3 class="section-title">🎤 ANALYSE DU PORTFOLIO ARTISTES</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Performance Commerciale</div>', unsafe_allow_html=True)
            self.create_sales_comparison_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">📈 Rentabilité par Artiste</div>', unsafe_allow_html=True)
            self.create_roi_chart()
        
        # Analyse détaillée par artiste
        st.markdown('<div class="subsection-title">🔍 Analyse Détailée par Artiste</div>', unsafe_allow_html=True)
        self.create_detailed_artist_analysis()

    def create_sales_comparison_chart(self):
        """Graphique de comparaison des ventes"""
        artists = list(self.artists_data.keys())
        ventes = [self.financial_data[artist]['ventes_albums'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=artists,
            y=ventes,
            marker_color=[self.color_palette[artist] for artist in artists],
            text=[f"{v/1000000:.1f}M" for v in ventes],
            textposition='auto',
            textfont=dict(color='white', size=14, weight='bold')
        ))
        
        fig.update_layout(
            title='Ventes Totalisées par Artiste',
            xaxis_title='Artistes',
            yaxis_title="Nombre d'albums vendus",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_roi_chart(self):
        """Graphique du retour sur investissement"""
        artists = list(self.financial_data.keys())
        roi = [self.financial_data[artist]['roi'] for artist in artists]
        rentabilite = [self.financial_data[artist]['rentabilite'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[roi[i]],
                y=[rentabilite[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=12, weight='bold'),
                name=artist,
                showlegend=True
            ))
        
        fig.update_layout(
            title='ROI vs Rentabilité',
            xaxis_title='Retour sur Investissement (%)',
            yaxis_title='Taux de Rentabilité (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#C0C0C0',
                borderwidth=1,
                font=dict(color='white', size=10)
            ),
            xaxis=dict(range=[250, 1200], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[60, 100], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_artist_analysis(self):
        """Analyse détaillée par artiste"""
        artists = list(self.artists_data.keys())
        tabs = st.tabs(artists)
        
        for i, artist in enumerate(artists):
            with tabs[i]:
                couleur = self.color_palette[artist]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Informations générales
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{artist}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">{self.artists_data[artist]['genre']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Métriques clés
                    st.metric("Albums chez Bad Boy", self.artists_data[artist]['albums_badboy'])
                    st.metric("Ventes totales", f"{self.financial_data[artist]['ventes_albums']:,}")
                    st.metric("Chiffre d'affaires", f"{self.financial_data[artist]['chiffre_affaires']/1000000:.2f}M$")
                    
                    # Succès principal
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Succès Principal:</div>
                        <div style="color: #ffffff; font-style: italic; font-size: 1.1rem;">{self.artists_data[artist]['succes_principal']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Caractéristiques commerciales
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Performance Commerciale:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                            <li>Rentabilité: {self.financial_data[artist]['rentabilite']}%</li>
                            <li>ROI: {self.financial_data[artist]['roi']}%</li>
                            <li>Coût production moyen: {self.financial_data[artist]['cout_production_moyen']/1000:.0f}k$</li>
                            <li>Budget marketing moyen: {self.financial_data[artist]['budget_marketing_moyen']/1000:.0f}k$</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Graphique radar des caractéristiques
                    categories = ['Ventes', 'Rentabilité', 'ROI', 'Impact']
                    valeurs = [
                        min(100, self.financial_data[artist]['ventes_albums'] / 250000),  # Normalisé
                        self.financial_data[artist]['rentabilite'],
                        min(100, self.financial_data[artist]['roi'] / 12),  # Normalisé
                        100 if self.artists_data[artist]['impact'] in ['Visionnaire commercial', 'Icône du hip-hop East Coast', 'Pionnière du rap féminin'] else 
                        85 if self.artists_data[artist]['impact'] in ['Style unique', 'Voix soul distinctive'] else
                        70
                    ]
                    
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatterpolar(
                        r=valeurs + [valeurs[0]],
                        theta=categories + [categories[0]],
                        fill='toself',
                        line=dict(color=couleur, width=3),
                        marker=dict(size=8, color=couleur),
                        name=artist
                    ))
                    
                    fig.update_layout(
                        polar=dict(
                            bgcolor='#1a1a1a',
                            radialaxis=dict(
                                visible=True, 
                                range=[0, 100],
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            ),
                            angularaxis=dict(
                                gridcolor='#333333',
                                tickfont=dict(color='#ffffff', size=12),
                                linecolor='#444444'
                            )
                        ),
                        paper_bgcolor='#0a0a0a',
                        font=dict(color='#ffffff', size=14),
                        showlegend=False,
                        height=300,
                        title=f"Profil de Performance - {artist}"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)

    def create_production_analysis(self):
        """Analyse de la production"""
        st.markdown('<h3 class="section-title">🏭 ANALYSE DE LA PRODUCTION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📅 Cycles de Production</div>', unsafe_allow_html=True)
            self.create_production_timeline()
        
        with col2:
            st.markdown('<div class="subsection-title">⚙️ Qualité et Support</div>', unsafe_allow_html=True)
            self.create_quality_support_chart()
        
        # Analyse des coûts
        st.markdown('<div class="subsection-title">💰 Analyse des Coûts de Production</div>', unsafe_allow_html=True)
        self.create_cost_analysis()

    def create_production_timeline(self):
        """Timeline de la production"""
        artists = list(self.production_data.keys())
        durees = [self.production_data[artist]['duree_contrat'] for artist in artists]
        albums = [self.production_data[artist]['albums_produits'] for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[durees[i]],
                y=[albums[i]],
                mode='markers+text',
                marker=dict(
                    size=60, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=2, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Durée des Contrats vs Nombre d\'Albums',
            xaxis_title='Durée du contrat (années)',
            yaxis_title="Nombre d'albums produits",
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_quality_support_chart(self):
        """Graphique qualité vs support"""
        artists = list(self.production_data.keys())
        qualite = [self.production_data[artist]['qualite_production'] for artist in artists]
        support = [self.production_data[artist]['support_label'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=qualite,
            y=support,
            mode='markers+text',
            marker=dict(
                size=60,
                color=[self.color_palette[artist] for artist in artists],
                opacity=0.9
            ),
            text=artists,
            textposition="top center",
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            title='Qualité de Production vs Support du Label',
            xaxis_title='Qualité de Production (1-10)',
            yaxis_title='Support du Label (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[6, 10.5], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[5, 10.5], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_cost_analysis(self):
        """Analyse des coûts de production"""
        artists = list(self.financial_data.keys())
        couts_production = [self.financial_data[artist]['cout_production_moyen'] for artist in artists]
        budgets_marketing = [self.financial_data[artist]['budget_marketing_moyen'] for artist in artists]
        ventes = [self.financial_data[artist]['ventes_albums'] for artist in artists]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Coût Production',
            x=artists,
            y=couts_production,
            marker_color='#C0C0C0',
            text=[f"{v/1000:.0f}k$" for v in couts_production],
            textposition='auto',
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.add_trace(go.Bar(
            name='Budget Marketing',
            x=artists,
            y=budgets_marketing,
            marker_color='#FFD700',
            text=[f"{v/1000:.0f}k$" for v in budgets_marketing],
            textposition='auto',
            textfont=dict(color='white', size=10, weight='bold')
        ))
        
        fig.update_layout(
            barmode='group',
            title='Répartition des Coûts par Artiste',
            xaxis_title='Artistes',
            yaxis_title='Montant ($)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#C0C0C0',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(tickfont=dict(size=10), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=10), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_analysis(self):
        """Analyse des stratégies marketing"""
        st.markdown('<h3 class="section-title">🎯 ANALYSE DES STRATÉGIES MARKETING</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📢 Budgets Marketing</div>', unsafe_allow_html=True)
            self.create_marketing_budget_chart()
        
        with col2:
            st.markdown('<div class="subsection-title">🎪 Canaux de Distribution</div>', unsafe_allow_html=True)
            self.create_marketing_channels_analysis()
        
        # Analyse détaillée par stratégie
        st.markdown('<div class="subsection-title">🔍 Analyse par Stratégie Marketing</div>', unsafe_allow_html=True)
        self.create_detailed_marketing_analysis()

    def create_marketing_budget_chart(self):
        """Graphique des budgets marketing"""
        artists = list(self.marketing_data.keys())
        budget_ratios = [self.marketing_data[artist]['budget_ratio'] for artist in artists]
        succes = [10 if self.marketing_data[artist]['succes'] == 'Légendaire' else 
                 9 if self.marketing_data[artist]['succes'] == 'Exceptionnel' else
                 8 if self.marketing_data[artist]['succes'] == 'Très bon' else
                 7 if self.marketing_data[artist]['succes'] == 'Bon' else
                 6 if self.marketing_data[artist]['succes'] == 'Modéré' else
                 5 for artist in artists]
        
        fig = go.Figure()
        
        for i, artist in enumerate(artists):
            fig.add_trace(go.Scatter(
                x=[budget_ratios[i]],
                y=[succes[i]],
                mode='markers+text',
                marker=dict(
                    size=80, 
                    color=self.color_palette[artist], 
                    opacity=0.9,
                    line=dict(width=3, color='#ffffff')
                ),
                text=[artist],
                textposition="middle center",
                textfont=dict(color='white', size=10, weight='bold'),
                name=artist
            ))
        
        fig.update_layout(
            title='Budget Marketing vs Succès Commercial',
            xaxis_title='Ratio Budget Marketing (%)',
            yaxis_title='Niveau de Succès (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400,
            showlegend=False,
            xaxis=dict(range=[15, 35], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[5, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_marketing_channels_analysis(self):
        """Analyse des canaux marketing"""
        # Compter les canaux les plus utilisés
        canaux_count = {}
        for artist_data in self.marketing_data.values():
            for canal in artist_data['canaux']:
                canaux_count[canal] = canaux_count.get(canal, 0) + 1
        
        canaux = list(canaux_count.keys())
        counts = list(canaux_count.values())
        
        fig = go.Figure(go.Bar(
            x=counts,
            y=canaux,
            orientation='h',
            marker_color='#9370DB',
            text=counts,
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title='Canaux Marketing les Plus Utilisés',
            xaxis_title="Nombre d'artistes utilisant le canal",
            yaxis_title='Canaux Marketing',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def create_detailed_marketing_analysis(self):
        """Analyse marketing détaillée"""
        artists = list(self.marketing_data.keys())
        tabs = st.tabs(artists)
        
        for i, artist in enumerate(artists):
            with tabs[i]:
                couleur = self.color_palette[artist]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Stratégie marketing
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, {couleur}20 0%, {couleur}05 100%); padding: 1rem; border-radius: 8px; border-left: 5px solid {couleur}; margin-bottom: 1rem;">
                        <div style="color: {couleur}; font-weight: bold; font-size: 1.5rem; margin-bottom: 0.5rem;">{artist}</div>
                        <div style="color: #cccccc; font-size: 1.1rem; font-weight: 500;">Stratégie Marketing</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.metric("Stratégie", self.marketing_data[artist]['strategie'])
                    st.metric("Budget Ratio", f"{self.marketing_data[artist]['budget_ratio']}%")
                    st.metric("Succès", self.marketing_data[artist]['succes'])
                    
                    # Cibles
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Public Cible:</div>
                        <div style="color: #ffffff; font-weight: 500;">{self.marketing_data[artist]['cibles']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Canaux utilisés
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Canaux Principaux:</div>
                        <ul style="color: #ffffff; font-weight: 500;">
                    """, unsafe_allow_html=True)
                    
                    for canal in self.marketing_data[artist]['canaux']:
                        st.markdown(f"<li>{canal}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                    
                    # Innovations
                    st.markdown(f"""
                    <div style="background: #1a1a1a; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #333333;">
                        <div style="font-weight: bold; color: {couleur}; margin-bottom: 0.5rem;">Innovations:</div>
                        <div style="color: #ffffff; font-weight: 500;">{self.marketing_data[artist]['innovations']}</div>
                    </div>
                    """, unsafe_allow_html=True)

    def create_management_analysis(self):
        """Analyse de la gestion et management"""
        st.markdown('<h3 class="section-title">🏢 ANALYSE DE LA GESTION</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="subsection-title">📊 Structure Organisationnelle</div>', unsafe_allow_html=True)
            self.create_org_structure()
        
        with col2:
            st.markdown('<div class="subsection-title">💼 Modèle Économique</div>', unsafe_allow_html=True)
            self.create_economic_model()
        
        # Analyse SWOT
        st.markdown('<div class="subsection-title">🔍 Analyse SWOT du Label</div>', unsafe_allow_html=True)
        self.create_swot_analysis()

    def create_org_structure(self):
        """Structure organisationnelle"""
        # Créer un graphique pour la structure organisationnelle
        fig = go.Figure()
        
        # Ajouter les données pour l'organigramme
        fig.add_trace(go.Scatter(
            x=[1, 2, 3, 4, 5],
            y=[1, 1, 1, 1, 1],
            mode='markers+text',
            marker=dict(
                size=[40, 25, 25, 25, 25],
                color=['#FFD700', '#C0C0C0', '#4169E1', '#9370DB', '#FF6B6B'],
                opacity=0.9,
                line=dict(width=2, color='#ffffff')
            ),
            text=['CEO', 'A&R', 'Marketing', 'Mode', 'Production'],
            textposition="middle center",
            textfont=dict(color='white', size=12, weight='bold'),
            showlegend=False
        ))
        
        # Ajouter les lignes de connexion
        fig.add_shape(type="line", x0=1, y0=1, x1=5, y1=1, line=dict(color="#ffffff", width=2))
        
        fig.update_layout(
            title='Structure Organisationnelle',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=300,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Construire la liste des départements en HTML
        departments_html = "".join([f"<li>{dept}</li>" for dept in self.management_data['structure']['departements']])
        
        # Construire le HTML final en une seule chaîne propre
        html_card = f"""
        <div class="academic-card">
            <h4 style="color: #ffffff; text-align: center; font-weight: bold;">🏗️ STRUCTURE ORGANISATIONNELLE</h4>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="font-weight: 500;">
                    <strong style="color: #FFD700;">Type:</strong> {self.management_data['structure']['type']}
                </div>
                <div style="font-weight: 500;">
                    <strong style="color: #FFD700;">Effectif:</strong> {self.management_data['structure']['effectif']} personnes
                </div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #FFD700;">Départements:</strong>
                <ul style="color: #ffffff; font-weight: 500;">
                    {departments_html}
                </ul>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #FFD700;">Culture d'entreprise:</strong>
                <div style="color: #ffffff; font-weight: 500;">{self.management_data['structure']['culture_entreprise']}</div>
            </div>
        </div>
        """
        
        # Afficher le HTML avec le composant dédié
        components.html(html_card, height=250)

    def create_economic_model(self):
        """Modèle économique"""
        # Créer un graphique pour le modèle économique
        categories = ['Revenus', 'Coûts', 'Marge', 'Réinvestissement']
        valeurs = [100, 70, 30, 25]  # Valeurs en pourcentage
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=valeurs,
            marker_color=['#FFD700', '#C0C0C0', '#4169E1', '#9370DB'],
            text=[f"{v}%" for v in valeurs],
            textposition='auto',
            textfont=dict(color='white', size=12, weight='bold')
        ))
        
        fig.update_layout(
            title='Répartition Économique',
            xaxis_title='Catégories',
            yaxis_title='Pourcentage (%)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=300,
            showlegend=False,
            xaxis=dict(tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Construire le HTML final en une seule chaîne propre
        html_card = f"""
        <div class="academic-card">
            <h4 style="color: #ffffff; text-align: center; font-weight: bold;">💼 MODÈLE ÉCONOMIQUE</h4>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div style="font-weight: 500;">
                    <strong style="color: #C0C0C0;">Modèle:</strong> {self.management_data['finances']['model_economique']}
                </div>
                <div style="font-weight: 500;">
                    <strong style="color: #C0C0C0;">Marge nette:</strong> {self.management_data['finances']['marge_nette']}
                </div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #C0C0C0;">Investissement:</strong>
                <div style="color: #ffffff; font-weight: 500;">{self.management_data['finances']['investissement_artistes']}</div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong style="color: #C0C0C0;">Gestion du risque:</strong>
                <div style="color: #ffffff; font-weight: 500;">{self.management_data['finances']['risque']}</div>
            </div>
        </div>
        """
        
        # Afficher le HTML avec le composant dédié
        components.html(html_card, height=250)

    def create_swot_analysis(self):
        """Analyse SWOT"""
        # Créer un graphique radar pour l'analyse SWOT
        categories = ['Forces', 'Faiblesses', 'Opportunités', 'Menaces']
        valeurs = [9, 5, 8, 7]  # Scores sur 10
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=valeurs + [valeurs[0]],
            theta=categories + [categories[0]],
            fill='toself',
            line=dict(color='#FFD700', width=3),
            marker=dict(size=8, color='#FFD700'),
            name='Analyse SWOT'
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='#1a1a1a',
                radialaxis=dict(
                    visible=True, 
                    range=[0, 10],
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                ),
                angularaxis=dict(
                    gridcolor='#333333',
                    tickfont=dict(color='#ffffff', size=12),
                    linecolor='#444444'
                )
            ),
            paper_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            showlegend=False,
            height=400,
            title="Analyse SWOT du Label"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher les détails de l'analyse SWOT
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="academic-card puff-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">FORCES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Leadership visionnaire (P. Diddy)</li>
                    <li>Branding fort et reconnaissable</li>
                    <li>Portefeuille artistique diversifié</li>
                    <li>Capacité de crossover commercial</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card biggie-card">
                <h4 style="color: #C0C0C0; text-align: center; font-weight: bold;">FAIBLESSES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Dépendance au leader charismatique</li>
                    <li>Perte d'artistes clés au fil des ans</li>
                    <li>Image parfois trop commerciale</li>
                    <li>Concurrence pour les nouveaux talents</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="academic-card mase-card">
                <h4 style="color: #FF6B6B; text-align: center; font-weight: bold;">OPPORTUNITÉS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Rééditions et réinterprétations du catalogue</li>
                    <li>Partenariats avec marques de luxe</li>
                    <li>Contenus numériques et streaming</li>
                    <li>Expansion internationale</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="academic-card lilkim-card">
                <h4 style="color: #FF69B4; text-align: center; font-weight: bold;">MENACES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Évolution des goûts musicaux</li>
                    <li>Concurrence des labels indépendants</li>
                    <li>Changements dans l'industrie musicale</li>
                    <li>Vieillissement du catalogue principal</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def create_timeline_analysis(self):
        """Analyse chronologique"""
        st.markdown('<h3 class="section-title">📅 ANALYSE CHRONOLOGIQUE</h3>', unsafe_allow_html=True)
        
        # Créer un DataFrame pour la timeline
        df_timeline = pd.DataFrame(self.timeline_data)
        
        fig = go.Figure()
        
        # Ajouter les événements par type
        for event_type in df_timeline['type'].unique():
            df_type = df_timeline[df_timeline['type'] == event_type]
            fig.add_trace(go.Scatter(
                x=df_type['annee'],
                y=df_type['importance'],
                mode='markers+text',
                marker=dict(
                    size=df_type['importance'] * 8,
                    color=self.data_colors.get(event_type, '#ffffff'),
                    opacity=0.8,
                    line=dict(width=2, color='#ffffff')
                ),
                text=df_type['evenement'],
                textposition="top center",
                textfont=dict(color='white', size=10),
                name=event_type,
                showlegend=True
            ))
        
        fig.update_layout(
            title='Timeline Événements Clés du Label',
            xaxis_title='Année',
            yaxis_title='Importance (1-10)',
            paper_bgcolor='#1a1a1a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff', size=14),
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#C0C0C0',
                borderwidth=1,
                font=dict(color='white', size=12)
            ),
            xaxis=dict(range=[1992, 2020], tickfont=dict(size=12), gridcolor='#333333'),
            yaxis=dict(range=[0, 11], tickfont=dict(size=12), gridcolor='#333333')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau détaillé des événements
        st.markdown('<div class="subsection-title">📋 Détail des Événements</div>', unsafe_allow_html=True)
        
        # Formatage du tableau avec style
        st.markdown("""
        <style>
            .event-table {
                background-color: #1a1a1a;
                border-radius: 8px;
                padding: 1rem;
                margin-top: 1rem;
            }
            .event-row {
                display: grid;
                grid-template-columns: 80px 150px 1fr 100px;
                gap: 1rem;
                padding: 0.5rem 0;
                border-bottom: 1px solid #333333;
                color: #ffffff;
            }
            .event-header {
                font-weight: bold;
                color: #C0C0C0;
                border-bottom: 2px solid #C0C0C0;
                padding-bottom: 0.5rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="event-table">', unsafe_allow_html=True)
        st.markdown('<div class="event-row event-header"><div>Année</div><div>Type</div><div>Événement</div><div>Importance</div></div>', unsafe_allow_html=True)
        
        for event in self.timeline_data:
            color = self.data_colors.get(event['type'], '#ffffff')
            st.markdown(f"""
            <div class="event-row">
                <div style="color: {color}; font-weight: bold;">{event['annee']}</div>
                <div style="color: {color};">{event['type']}</div>
                <div>{event['evenement']}</div>
                <div style="color: {color};">{'⭐' * event['importance']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def create_conclusions(self):
        """Conclusions et recommandations"""
        st.markdown('<h3 class="section-title">📝 CONCLUSIONS ET RECOMMANDATIONS</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="academic-card puff-card">
                <h4 style="color: #FFD700; text-align: center; font-weight: bold;">🎯 POINTS CLÉS</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Bad Boy a redéfini le hip-hop commercial dans les années 90</li>
                    <li>Modèle économique basé sur le branding et le luxe</li>
                    <li>Portefeuille équilibré entre hip-hop et R&B</li>
                    <li>L'héritage culturel reste fort malgré les défis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card biggie-card">
                <h4 style="color: #C0C0C0; text-align: center; font-weight: bold;">💡 LEÇONS APPRISES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>L'importance du branding cohérent</li>
                    <li>La valeur des partenariats stratégiques</li>
                    <li>La nécessité de se réinventer constamment</li>
                    <li>L'équilibre entre art et commerce</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="academic-card mase-card">
                <h4 style="color: #FF6B6B; text-align: center; font-weight: bold;">🚀 RECOMMANDATIONS STRATÉGIQUES</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Moderniser le catalogue pour le streaming</li>
                    <li>Développer de nouveaux talents</li>
                    <li>Explorer les collaborations intergénérationnelles</li>
                    <li>Capitaliser sur la nostalgie années 90-2000</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="academic-card lilkim-card">
                <h4 style="color: #FF69B4; text-align: center; font-weight: bold;">🔮 PERSPECTIVES D'AVENIR</h4>
                <ul style="color: #ffffff; font-weight: 500;">
                    <li>Transformation en hub de contenu multimédia</li>
                    <li>Expansion dans la mode et le lifestyle</li>
                    <li>Développement de projets autobiographiques</li>
                    <li>Positionnement comme label de référence historique</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    def run(self):
        """Fonction principale pour exécuter le dashboard"""
        self.display_header()
        
        # Créer les onglets principaux
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🎤 Artistes", 
            "🏭 Production", 
            "🎯 Marketing", 
            "🏢 Gestion", 
            "📅 Timeline", 
            "📝 Conclusions"
        ])
        
        with tab1:
            self.create_artist_analysis()
        
        with tab2:
            self.create_production_analysis()
        
        with tab3:
            self.create_marketing_analysis()
        
        with tab4:
            self.create_management_analysis()
        
        with tab5:
            self.create_timeline_analysis()
        
        with tab6:
            self.create_conclusions()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); border-radius: 10px; border: 1px solid #444444;">
            <p style="color: #C0C0C0; font-weight: bold; font-size: 1.2rem;">BAD BOY RECORDS - Dashboard Stratégique</p>
            <p style="color: #cccccc; margin-top: 0.5rem;">Analyse complète 1993-2024 | Label de hip-hop américain</p>
            <div style="margin-top: 1rem;">
                <span class="badboy-badge">P. DIDDY</span>
                <span class="badboy-badge">BIGGIE</span>
                <span class="badboy-badge">BAD BOY FAMILY</span>
            </div>
            <p style="color: #999999; margin-top: 1rem; font-size: 0.9rem;">© 2024 - Tous droits réservés</p>
        </div>
        """, unsafe_allow_html=True)

# Point d'entrée principal
if __name__ == "__main__":
    analyzer = BadBoyAnalyzer()
    analyzer.run()
