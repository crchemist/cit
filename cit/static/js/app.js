var app = angular.module('CITApp', ['pascalprecht.translate']);

app.config(function ($translateProvider) {
  var language = ((window.navigator.userLanguage ||
                  window.navigator.browserLanguage ||
                  window.navigator.language).toLowerCase()).split('-')[0];
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
  $translateProvider.preferredLanguage(language);
  $translateProvider.fallbackLanguage('uk');
});
