import Head from "next/head"
import Units from "../components/units"

export default function Home({ unitData }) {
    const unitsHashMap = {}

    let i = 0
    for (const unit of unitData.units) {
        for (const name of unit.names) {
            unitsHashMap[name] = i
        }
        i++
    }

    return (
        <>
            <Head>
                <title>EF Unit generator</title>
                <link rel="shortcut icon" href="/favicon.png"></link>
            </Head>
            <Units unitsHashMap={unitsHashMap} unitData={unitData} />
        </>
    )
}

export async function getStaticProps() {
    const res = await fetch(process.env.NEXT_PUBLIC_DOMAIN_NAME + "units.json")
    const unitData = await res.json()


    return {
        props: {
            unitData
        }
    }
}
