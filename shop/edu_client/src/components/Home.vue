<template>
    <div>
         <Header></Header>
        <Banner></Banner>
        <Fotter></Fotter>
    </div>
</template>

<script>
    import Header from "./Header";
    import Banner from "./Banner";
    import Fotter from "./Fotter";

    export default {
        name: "Home",
        components: {
            "Header": Header,
            "Banner": Banner,
            "Fotter": Fotter,
        }
    }
</script>

<style scoped>

</style>
