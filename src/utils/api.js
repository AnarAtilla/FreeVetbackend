import axios from 'axios';

// базовый URL
const API_BASE_URL = 'https://freevetback.ru/';

// Создаем экземпляр axios с базовыми настройками для формата Json
const apiClientJson = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Создаем экземпляр axios с базовыми настройками для формата Multi
const apiClientMultipart = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

// 1. users/login/google/ - регистрация и вход google через редирект
export const loginUserGoogle = () => {
  // Редирект на серверный маршрут, который ведет на Google OAuth
  window.location.href = `${API_BASE_URL}users/login/google/`;
};

// 2. users/login/facebook/ - регистрация и вход facebook через редирект
export const loginUserFacebook = () => {
  // Редирект на серверный маршрут, который ведет на Facebook OAuth
  window.location.href = `${API_BASE_URL}users/login/facebook/`;
};

// 3. users/register/ - регистрация по телефону
export const createUser = async (data) => {
  try {
    const response = await apiClientMultipart.post('users/register/', data);
    return response.data;
  } catch (error) {
    console.error('Ошибка создания юзера:', error);
    throw error;
  }
};

// 4. users/login/ - вход по телефону
export const loginUserPhone = async (data) => {
  try {
    const response = await apiClientJson.post('users/login/', data);
    return response.data;
  } catch (error) {
    console.error('Ошибка входа:', error);
    throw error;
  }
};

// 5. users/verify/ - верификация по смс
export const verifyUserSMS = async (data) => {
  try {
    const response = await apiClientJson.post('users/verify/ ', data);
    return response.data;
  } catch (error) {
    console.error('Ошибка верификации:', error);
    throw error;
  }
};

// 6. questions/add/ - отправка вопроса  
export const addQuestion = async (data) => {
  try {
    const response = await apiClientMultipart.post('questions/add/', data);
    return response.data;
  } catch (error) {
    console.error('Ошибка отправки вопроса:', error);
    throw error;
  }
};
