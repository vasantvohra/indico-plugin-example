import React from 'react';
import {bindTranslateComponents} from 'indico/react/i18n';


const {Translate} = bindTranslateComponents('example');

const getJSX = () => (
    <Translate>This message was generated using JavaScript</Translate>
);

export default getJSX;
