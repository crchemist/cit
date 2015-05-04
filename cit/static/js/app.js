var app = angular.module('CITApp', ['ngRoute','ngLocale','pascalprecht.translate']);

app.config(function ($translateProvider) {
  var language = ((window.navigator.userLanguage ||
                  window.navigator.browserLanguage ||
                  window.navigator.language).toLowerCase()).split('-')[0];
    $translateProvider.translations('uk', {
      TITLE: 'Моніторинг громадських проблем',
      SIGN_IN_WITH_FACEBOOK: 'Увійти через Facebook',
      LOGOUT: 'Вийти',
      HOME: 'Головна',
      LOGO: 'Логотип'
  });
    $translateProvider.translations('ru', {
      TITLE: 'Мониторинг общественных проблем',
      SIGN_IN_WITH_FACEBOOK: 'Ввойти через Facebook',
      LOGOUT: 'Выйти',
      HOME: 'Главная',
      LOGO: 'Логотип'
  });
    $translateProvider.translations('en', {
      TITLE: 'Civic Issue Tracker',
      SIGN_IN_WITH_FACEBOOK: 'Sign in with Facebook',
      LOGOUT: 'Logout',
      HOME: 'Home',
      LOGO: 'Logo'
  });
  
    $translateProvider.preferredLanguage(language);
    $translateProvider.fallbackLanguage('uk');
});