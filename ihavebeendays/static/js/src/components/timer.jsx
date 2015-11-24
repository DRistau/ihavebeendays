import React from 'react';
import moment from 'moment';

class Timer extends React.Component {
    constructor(props) {
        super(props);

        this.startingAt = moment.utc(props.startingAt, 'YYYY-MM-DDThh:mm:ssZ');
    }

    componentDidMount() {
        setInterval(() => {
            this.setState({});
        }, this.props.interval);
    }

    render() {
        let fromNow = this.startingAt.fromNow(true);

        return (
            <span>{fromNow}</span>
        );
    }
}
export default Timer;
