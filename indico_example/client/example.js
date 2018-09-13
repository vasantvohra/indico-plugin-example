import ReactDOM from 'react-dom';

import {$T} from 'indico/utils/i18n';
import './example.scss';
import getJSX from './example.jsx';


alert('hi');
$(document).ready(() => {
    const $t = $T.domain('example');
    $('#js-msg').text($t.gettext('This message was generated using JavaScript'));
    $('#yes-msg').text($T.gettext('Edit'));
    ReactDOM.render(getJSX(), document.getElementById('jsx-msg'));
});
