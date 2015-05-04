    
var app = angular.module('CITApp', ['ngRoute','ngLocale','pascalprecht.translate']);


app.config(function ($translateProvider) {
  $translateProvider.translations('uk', {
    SIGN_IN_WITH_FACEBOOK: 'Увійти через Facebook',
    LOGOUT: 'Вийти',
    HOME: 'Головна',
    LOGO: 'Логотип'
  });
   $translateProvider.translations('en', {
    SIGN_IN_WITH_FACEBOOK: 'Sign in with Facebook',
    LOGOUT: 'Logout',
    HOME: 'Home',
    LOGO: 'Logo'
  });
  $translateProvider.translations('ru', {
    SIGN_IN_WITH_FACEBOOK: 'Ввойти через Facebook',
    LOGOUT: 'Выйти',
    HOME: 'Главная',
    LOGO: 'Логотип'
  });
  $translateProvider.preferredLanguage('uk');
});

