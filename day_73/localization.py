"""
Localization module for WalkPal application.
Handles translation of all user-facing strings and AI prompts.
"""

import logging
from typing import Dict, Any, Optional

# Set up logging
logger = logging.getLogger(__name__)

# Supported languages and their metadata
SUPPORTED_LANGUAGES = {
    'en': {
        'code': 'en-US',
        'name': 'English',
        'native_name': 'English',
        'system_code': 'en-US',
        'available': True
    },
    'es': {
        'code': 'es-ES',
        'name': 'Spanish',
        'native_name': 'Español',
        'system_code': 'es-ES',
        'available': True
    },
    'fr': {
        'code': 'fr-FR',
        'name': 'French',
        'native_name': 'Français',
        'system_code': 'fr-FR',
        'available': False
    },
    'hi': {
        'code': 'hi-IN',
        'name': 'Hindi',
        'native_name': 'हिंदी',
        'system_code': 'hi-IN',
        'available': False
    }
}

# Default language (used as fallback)
DEFAULT_LANGUAGE = 'en'

# Localization dictionary
localization_dict = {
    # English (default)
    'en': {
        # UI Strings
        'ui': {
            # Main Menu
            'welcome': "Welcome to WalkPal!",
            'menu_title': "What would you like to do?",
            'menu_start_walk': "Start a Walk",
            'menu_manage_data': "Manage Data",
            'menu_exit': "Exit",
            'prompt_choice': "Enter your choice ({range}): ",
            'invalid_choice': "Invalid choice. Please try again.",
            
            # Walk Preferences
            'prompt.duration': "How long is your walk? (in minutes)",
            'prompt.duration_quick_select': "Quick select: {quick_options}",
            'prompt.duration_examples': "Or enter any whole number (e.g., 2, 7, 20, 45, etc.)",
            'prompt.duration_input': "\nEnter walk duration (minutes): ",
            'message.invalid_number': "Please enter a valid number.",
            'message.invalid_duration': "Please enter a positive number.",
            
            'prompt.mood_header': "What kind of vibe are you looking for on this walk?",
            'prompt.mood_options': "Options: {options}",
            'prompt.custom_topic_example': "Or enter a custom topic (e.g., 'story of vijay mallya', 'ramayan', 'business tactics by tim cook', 'comedy')",
            'prompt.mood_input': "Enter your mood choice [{default}]: ",
            'message.invalid_mood': "Invalid mood choice. Please choose from: {options} or enter a custom topic. Using default: {default_mood}",
            
            'prompt.output_mode': "Choose output mode: (Text / Audio): ",
            'message.invalid_output_mode': "Please enter either 'text' or 'audio'.",
            
            # Walk Summary
            'message.walk_summary': "Planning your {duration}-minute walk with a '{mood}' vibe...",
            'content.header': "--- WalkPal Content ---",
            'message.no_content': "No content was generated.",
            'message.tts_failed_fallback': "Failed to speak content. Using text output.",
            'message.audio_disabled_fallback': "Audio mode selected.",
            'message.enjoy_walk': "Enjoy your walk!",
            
            # Content Generation
            'message.starting_generation': "\nStarting content generation...",
            'message.generating_complete_content': "\nGenerating complete content for {duration} minutes...",
            'content.complete_header': "\n--- Complete Content Generated (~{estimated_time:.1f} min) ---",
            'message.generating_chunk': "\nGenerating content chunk for ~{target_duration:.1f} minutes...",
            'content.chunk_header': "\n--- Chunk Generated (~{estimated_time:.1f} min) ---",
            'message.content_generation_error': "Error generating content: {error}",
            'message.preparing_walk': "Planning your {duration}-minute walk with a '{mood}' vibe...",
            'prompt.want_more': "Would you like to hear more? (y/n): ",
            'message.stopping_generation': "\nStopping content generation as requested.",
            
            # Feedback
            'feedback_prompt': "\nHow was this session? (1-5 stars, or press Enter to skip): ",
            'feedback_skipped': "Skipping feedback.",
            'feedback_invalid_input': "Invalid input. Please enter a number or press Enter to skip.",
            'feedback_invalid_score': "Invalid input. Please enter a number between 1 and 5.",
            'feedback.prompt': "\nHow was this session? (1-5 stars, or press Enter to skip): ",
            
            # Data Management
            'data_management': {
                'menu_header': "\n--- Data Management Menu ---",
                'exporting': "\nExporting walk history...",
                'filename_prompt': "Enter a filename for the export (e.g., 'walk_history_2024-01-01.json'): ",
                'export_success': "\nWalk history exported successfully!",
                'export_failed': "\nExport failed.",
                'creating_backup': "\nCreating backup...",
                'backup_success': "\nBackup created successfully!",
                'backup_failed': "\nBackup failed.",
                'available_backups': "\nAvailable Backups:",
                'no_backups': "No backups found.",
                'restore_prompt': "Enter the number of the backup to restore (1-{count}): ",
                'restore_success': "\nBackup restored successfully!",
                'restore_failed': "\nRestore failed.",
                'invalid_backup': "\nInvalid backup number. Please try again.",
                'back_option': "4. Back to Main Menu",
                'choice_prompt': "\nEnter your choice (1-4): ",
                'export_option': "1. Export Walk History",
                'backup_option': "2. Create Backup",
                'restore_option': "3. Restore from Backup"
            },
                'back_option': "4. Back to Main Menu",
                'choice_prompt': "\nEnter your choice (1-4): ",
                'export_option': "1. Export Walk History",
                'backup_option': "2. Create Backup",
                'restore_option': "3. Restore from Backup",
            },
            
            # Interactive Loop
            'prompt_want_more': "\nTotal content so far ~{total_estimated_time:.1f}/{target_duration:.1f} min. Continue? (y/N): ",
            'no_backups': "No backups found.",
            
            # Error Messages
            'error_generic': "Error: {message}",
            'error_file_not_found': "File not found: {filename}",
            'error_invalid_input': "Invalid input: {message}",
            'error_tts_unavailable': "Voice output will be unavailable.",
            
            # Loading/Analysis
            'data_load_start': "=== Starting data load and analysis ===",
            'loading_log': "Loading walk log...",
            'log_entries_loaded': "Loaded {count} log entries",
            'analyzing_data': "Analyzing session data...",
            'analysis_complete': "Analysis complete. Total sessions: {count}",
            'error_analysis': "ERROR in load_and_analyze_data_globally: {message}",
            
            # Goodbye
            'goodbye': "Thank you for using WalkPal! Goodbye!",
        },
        
        # Mood Names
        'moods': {
            # Default mood
            'default': {
                'name': 'Unknown Mood',
                'description_tag': 'general, engaging content'
            },
            
            # Learn mood
            'learn': {
                'name': 'Learn Something New',
                'description_tag': 'factual, educational, insightful'
            },
            
            # Reflect mood
            'reflect': {
                'name': 'Reflect & Reset',
                'description_tag': 'calming, mindful, introspective, question-based'
            },
            
            # Story mood
            'story': {
                'name': 'Storytime',
                'description_tag': 'narrative, engaging, short story, anecdote'
            },
            
            # Humor mood
            'humor': {
                'name': 'Make Me Laugh',
                'description_tag': 'joke, pun, funny fact, lighthearted'
            },
            
            # Surprise mood
            'surprise': {
                'name': 'Surprise Me!',
                'description_tag': 'unexpected, creative, mix of styles, delightful'
            },
            
            # Custom mood
            'custom': {
                'name': 'Custom Topic',
                'description_tag': 'specific topic, personalized content'
            }
        },
        
        # AI Prompts and Instructions
        'prompts': {
            'system': "You are WalkPal, an AI-powered walking companion that generates engaging content for users while they walk. You provide thoughtful, personalized content based on the user's mood and preferences. Your responses are clear, concise, and appropriate for the chosen mood.",
            
            # Mood-specific tasks
            'tasks': {
                'learn': {
                    'base': "Generate informative and engaging content about the chosen topic. Keep it interesting and relevant to the user's current walk.",
                    'language': "Respond in {language_name} while maintaining the same informative style.",
                },
                'reflect': {
                    'base': "Create thought-provoking content that encourages self-reflection and mindfulness during the walk.",
                    'language': "Respond in {language_name} while maintaining the same reflective style.",
                },
                'story': {
                    'base': "Tell an engaging story that's appropriate for the duration of the walk.",
                    'language': "Respond in {language_name} while maintaining the same engaging storytelling style.",
                },
                'humor': {
                    'base': "Create funny and entertaining content that will make the user laugh during their walk.",
                    'language': "Respond in {language_name} while maintaining the same humorous style.",
                },
                'surprise': {
                    'base': "Generate unexpected and surprising content that keeps the user engaged and entertained.",
                    'language': "Respond in {language_name} while maintaining the same surprising and engaging style.",
                },
                'custom': {
                    'base': "Generate content specifically about the user's custom topic in a style that matches their mood.",
                    'language': "Respond in {language_name} while maintaining the same personalized style.",
                },
            },
            
            # Conversation management
            'conversation': {
                'context': "The user is currently on a {duration}-minute walk and has chosen the {mood} mood.",
                'history': "Previous conversation history: {history}",
                'continuation': "Continue the conversation in the same style and language.",
            },
            
            # Error handling
            'errors': {
                'invalid_input': "Please provide valid input for {field}.",
                'generation_failed': "Failed to generate content. Please try again.",
                'invalid_mood': "Invalid mood specified: {mood}",
            },
        },
        
        # Insights and Analysis
        'insights': {
            'header': "--- Your Walk History Insights ---",
            'most_frequent': "- Your most frequent mood is '{mood}' ({percentage}% of walks).",
            'time_preference': "- You often prefer '{mood}' during {time_block}.",
            'highest_rated': "- Your highest rated mood is '{mood}' with an average rating of {rating}/5.0 (based on {count} ratings).",
            'no_data': "No walk data available for insights.",
        }
    },
    
    # Spanish translations
    'es': {
        # UI Strings
        'ui': {
            'welcome': "¡Bienvenido a WalkPal!",
            'menu_title': "¿Qué te gustaría hacer?",
            'menu_start_walk': "Empezar un Paseo",
            'menu_manage_data': "Administrar Datos",
            'menu_exit': "Salir",
            'prompt_choice': "Ingrese su elección ({range}): ",
            'invalid_choice': "Elección inválida. Por favor, intente nuevamente.",
            'duration_prompt': "¿Cuánto tiempo durará tu paseo? (en minutos)",
            'duration_quick_select': "Selección rápida: {quick_options}",
            'duration_any_number': "O ingrese cualquier número entero (por ejemplo, 2, 7, 20, 45, etc.)",
            'mood_prompt': "¿Qué tipo de ambiente prefieres para este paseo?",
            'mood_options': "Opciones: {options}",
            'mood_custom_prompt': "O ingrese un tema personalizado (por ejemplo, 'historia de vijay mallya', 'ramayan', 'tácticas de negocios de tim cook', 'comedia')",
            'output_mode_prompt': "Elija el modo de salida: (Texto / Audio): ",
            'walk_summary': "Resumen del Paseo de {duration} minutos",
            'full_content': "--- Contenido Completo de WalkPal ({mood}) ---",
            'enjoy_walk': "¡Disfruta tu paseo!",
            'feedback_prompt': "¿Cómo fue esta sesión? (1-5 estrellas, o presione Enter para saltar): ",
            'feedback_saved': "¡Feedback ({rating} estrellas) guardado para el ID del paseo {walk_id}!",
            'data_exported': "Registro de paseos exportado a {filename}",
            'backup_created': "Copia de seguridad creada: {filename}",
            'select_backup': "Seleccione una copia de seguridad para restaurar (o '0' para cancelar): ",
            'restore_cancelled': "Restauración cancelada.",
            'invalid_backup': "Selección de copia de seguridad inválida.",
            'restore_success': "Restauración exitosa desde la copia de seguridad: {filename}",
            'no_backups': "No se encontraron archivos de copia de seguridad.",
            'goodbye': "¡Gracias por usar WalkPal! ¡Adiós!",
        },
        
        # Mood names and descriptions
        'moods': {
            'learn': {
                'name': 'Aprender Algo Nuevo',
                'description': 'Obtener hechos y conocimientos interesantes',
            },
            'reflect': {
                'name': 'Reflexionar y Resetear',
                'description': 'Contenido reflexivo para la atención plena',
            },
            'story': {
                'name': 'Hora de Historias',
                'description': 'Historias y narrativas atractivas',
            },
            'humor': {
                'name': 'Hazme Reír',
                'description': 'Contenido divertido y entretenido',
            },
            'surprise': {
                'name': '¡Sorpréndeme!',
                'description': 'Una mezcla de diferentes tipos de contenido',
            },
            'custom': {
                'name': 'Tema Personalizado',
                'description': 'Tu tema elegido',
            },
        },
        
        # AI Prompts
        'prompts': {
            'system': """Eres WalkPal, un compañero de paseos amistoso y conocedor.
Tu objetivo es proporcionar contenido conversacional y atractivo que haga que los paseos sean más agradables y productivos.
Mantén las respuestas naturales, amigables y apropiadas para escuchar mientras caminas.
Enfócate en entregar contenido valioso de manera clara y accesible.
""",
            'tasks': {
                'learn': "Proporciona un contenido interesante y educativo sobre {topic}. Hazlo atractivo y fácil de entender mientras caminas.",
                'reflect': "Ofrece una reflexión o ejercicio de atención plena sobre {topic}. Manténlo introspectivo y calmante.",
                'story': "Cuenta una historia cautivadora sobre {topic}. Hazla atractiva con descripciones vívidas y una narrativa clara.",
                'humor': "Comparte algo divertido sobre {topic}. Manténlo ligero y apropiado para todo público.",
                'surprise': "Sorpréndeme con algo interesante sobre {topic}. Elige cualquier estilo que consideres más atractivo.",
                'custom': "Proporciona contenido atractivo sobre {topic}. Ajusta para que sea interesante y apropiado para un paseo.",
            },
            'language_instruction': "Genera la respuesta estrictamente en {language}."
        },
        
        # Insights and Analysis
        'insights': {
            'title': "--- Tu Historial de Paseos ---",
            'most_frequent_mood': "Tu estado de ánimo más frecuente es '{mood}' ({percentage}% de los paseos).",
            'mood_time_preference': "A menudo prefieres '{mood}' durante {time_of_day}.",
            'highest_rated_mood': "Tu estado de ánimo mejor calificado es '{mood}' con una calificación promedio de {rating}/5.0 (basado en {count} calificaciones).",
            'trend_stable': "Tus calificaciones de sesión son estables.",
            'trend_improving': "¡Tus calificaciones de sesión están mejorando recientemente!",
            'trend_declining': "Tus calificaciones de sesión están disminuyendo recientemente.",
        },
    },
    
    # French translations (partial - to be completed)
    'fr': {
        # Add French translations here
    },
    
    # Hindi translations (partial - to be completed)
    'hi': {
        # Add Hindi translations here
    }
}



def get_text(key, lang=DEFAULT_LANGUAGE, **kwargs):
    """
    Retrieve a localized string by key.
    
    Args:
        key (str): The key to look up in the translations
        lang (str, optional): The language code to use. Defaults to DEFAULT_LANGUAGE
        **kwargs: Any format arguments to be passed to str.format()
        
    Returns:
        str: The localized string, or a fallback if not found
    """
    try:
        # Start with the requested language
        lang_dict = localization_dict.get(lang, {})
        if not lang_dict:
            # If language not found, fall back to English
            lang_dict = localization_dict.get('en', {})
            if not lang_dict:
                logger.error(f"No translations found for any language (key: {key})")
                return f"[Missing translation for key: {key}]"
        
        # Handle UI strings by looking them up directly in the UI section
        if key.startswith('ui.'):
            # Split the key into 'ui' and the rest
            parts = key.split('.', 1)
            if len(parts) == 2:
                ui_dict = lang_dict.get('ui', {})
                if isinstance(ui_dict, dict):
                    # Look up the rest of the key in the UI section
                    return ui_dict.get(parts[1], f"[Missing translation for key: {key}]")
        
        # Try to get the value directly
        value = lang_dict.get(key)
        if value is not None and isinstance(value, str):
            try:
                return value.format(**kwargs) if kwargs else value
            except KeyError as ke:
                logger.error(f"Missing format parameter in translation: {key} - {str(ke)}")
                return f"[Error in translation format: {key}]"
        
        # If not found, try English fallback
        if lang != 'en':
            return get_text(key, 'en', **kwargs)
            
        logger.error(f"Translation not found for key: {key}")
        return f"[Missing translation for key: {key}]"
        
    except Exception as e:
        logger.error(f"Error in get_text: {e}")
        if lang != 'en':
            return get_text(key, 'en', **kwargs)
        return f"[Error retrieving translation for key: {key}]"


def get_supported_languages() -> Dict[str, Dict[str, str]]:
    """Get the list of supported languages."""
    return SUPPORTED_LANGUAGES

def get_language_name(lang_code: str) -> str:
    """Get the name of a language in its native language."""
    return SUPPORTED_LANGUAGES.get(lang_code, {}).get('native_name', lang_code)

def get_language_code(lang_code: str) -> str:
    """Get the BCP 47 language code for a language."""
    return SUPPORTED_LANGUAGES.get(lang_code, {}).get('code', lang_code)

def is_language_supported(lang_code: str) -> bool:
    """Check if a language is supported."""
    return lang_code in SUPPORTED_LANGUAGES
