<template>
<div id="vehicle-data-wrapper">
    <div class="header">
        <h2>Table of Vehicle Data</h2>
    </div>
    <div class="filters">
        <div class="input-group input-group-sm filter">
            <span class="input-group-text text-secondary bg-white">Vehicle ID</span>
            <select name="vehicleIdInput" id="vehicleIdInput">
                <option v-for="id in vehicle_ids" :value="id" v-bind:key="id">{{ id }}</option>
            </select>
        </div>
        <div class="input-group input-group-sm filter">
            <span class="input-group-text text-secondary bg-white">From</span>
            <Datepicker v-model="from"></Datepicker>
        </div>
        <div class="input-group input-group-sm filter">
            <span class="input-group-text text-secondary bg-white">To</span>
            <Datepicker v-model="to" ></Datepicker>
        </div>
        <button class="btn btn-primary">Filter</button>
    </div>
    <div class="table-wrapper">
        <table id="vehicle-data-table" class="table table-hover">
            <thead class="thead-dark">
                <tr>
                    <th>timestamp</th>
                    <th>speed</th>
                    <th>odometer</th>
                    <th>soc</th>
                    <th>elevation</th>
                    <th>shift_state</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="datapoint in datapoints" v-bind:key="datapoint.id">
                    <td>{{ datapoint.timestamp }}</td>
                    <td>{{ datapoint.speed }}</td>
                    <td>{{ datapoint.odometer }}</td>
                    <td>{{ datapoint.soc }}</td>
                    <td>{{ datapoint.elevation }}</td>
                    <td>{{ datapoint.shift_state.id }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
</template>

<script>

export default {
    data() {
        return {
            selected_vehicle: "123",
            vehicle_ids: [],
            from: null,
            to: null,
            datapoints: [{"id":451,"speed":200,"state_of_charge":50,"shift_state_id":"D","vehicle_id":"123","timestamp":"2023-01-19T14:25:12.336794","odometer":49923.2,"elevation":130,"shift_state":{"id":"D","name":"Drive"}}]
        };
    },
    methods: {
        updateDatapoints(){
            //TODO: call the API
            return
        },
    },
    computed: {
        sortedDatapoints(){
            //TODO: sort datapoints here
            return datapoints
        }
    },
    created() {
        //TODO: load data from API (pre-fill vehicle id dropdown)
    }
};
</script>

<style scoped>

.filters {
    display: flex;
    justify-content: center;
    align-content: center;
    flex-direction: row;
    flex-wrap: nowrap;
    align-items: center;

    padding-top: 20px;
    padding-bottom: 20px;

    border-bottom: 1px solid black;
    border-top: 1px solid black;
}

.filters > .filter {
    margin-right: 15px;
}

.table-wrapper {
    padding-top: 20px;
}

</style>