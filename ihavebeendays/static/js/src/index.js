import React from 'react';
import ReactDOM from 'react-dom';

import Timer from './components/timer.jsx';

let $timer = document.querySelector('#timer');

if ($timer) {
    let props = {
        startingAt: $timer.dataset.startingTime,
        interval: 1000 * 60
    };

    ReactDOM.render(<Timer {...props} />, $timer);
}
