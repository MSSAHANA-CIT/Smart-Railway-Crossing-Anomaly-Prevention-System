import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

import en from './locales/en/common.json'
import hi from './locales/hi/common.json'
import ta from './locales/ta/common.json'
import ml from './locales/ml/common.json'

const STORAGE_KEY = 'railway-crossing-lang'

const savedLanguage = localStorage.getItem(STORAGE_KEY) ?? 'en'

i18n.use(initReactI18next).init({
  resources: {
    en: { common: en },
    hi: { common: hi },
    ta: { common: ta },
    ml: { common: ml },
  },
  lng: savedLanguage,
  fallbackLng: 'en',
  defaultNS: 'common',
  interpolation: {
    escapeValue: false,
  },
})

i18n.on('languageChanged', (lng) => {
  localStorage.setItem(STORAGE_KEY, lng)
  document.documentElement.lang = lng
})

document.documentElement.lang = savedLanguage

export default i18n
