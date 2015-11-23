import React from 'react';
import moment from 'moment';

class Timer extends React.Component {
    render() {
        let startingAt = this.props.startingAt;
        let fromNow = moment.utc(startingAt, 'YYYY-MM-DDThh:mm:ssZ').fromNow(true);

        setInterval(() => {
            this.setState({});
        }, this.props.interval);

        return (
            <span>{fromNow}</span>
        );
    }
} 
export default Timer;
