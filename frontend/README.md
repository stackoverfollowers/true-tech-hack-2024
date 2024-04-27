# Шаблон React + TypeScript + Vite


## Стэк разработки

- React
- TypeScript
- [Effector](https://effector.dev/), [Effector patronum](https://patronum.effector.dev/)
- [React Router](https://reactrouter.com/)
- [ReactQuery](https://tanstack.com/query/latest)
- [MaterialUI](https://mui.com/)


## Развертывание проекта

[NPM v10](https://docs.npmjs.com/) и [NodeJS v20](https://nodejs.org/ru/)

1. Выполняем команду:

```shell
npm i
```

2. Запуск для разработки:

```shell
npm start
```

## Дополнительные команды

- Запуск тестов

```shell
npm run test
```

- Проверка ошибок связанных со стилем `JS/TS` кода

```shell
npm run lint
```

- Автоматическое исправление ошибок связанных со стилем `JS/TS` кода

```shell
npm run lint:fix
```

- Проверка ошибок связанных со стилем `CSS` кода

```shell
npm run stylelint
```

- Автоматическое исправление ошибок связанных со стилем `CSS` кода

```shell
npm run stylelint:fix
```

Прогонять линтеры в ручную необязательно, так как в проекте используется [husky](https://www.npmjs.com/package/husky) и
[lint-staged](https://www.npmjs.com/package/lint-staged) для запуска `pre-commit` хуков.

## Полезное

- [Соглашение о коммитах](https://www.conventionalcommits.org/ru/)
- [Семантического версионирования](https://semver.org/lang/ru/)
- [Архитектурная методология для фронтенд проектов](https://feature-sliced.design/ru/)
- Именованные экспорты вместо `default`
- Без вложенных тернарных операторов
- `SVG` файлы как `React` компоненты
