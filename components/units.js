import { useEffect, useState } from "react"
import styles from "../styles/Units.module.sass"
import { toPng } from "html-to-image"
import download from "downloadjs"

const Units = ({ unitsHashMap, unitData }) => {
    const [string, setString] = useState("")
    const [scale, setScale] = useState(1)

    const changeString = (scale) => {
        if (window) localStorage.setItem("string", scale)
        setString(scale)
    }

    const changeScale = (scale) => {
        if (window) localStorage.setItem("scale", scale)
        setScale(scale)
    }

    useEffect(() => {
        let savedScale = localStorage.getItem("scale")
        if (savedScale) setScale(savedScale)

        let savedString = localStorage.getItem("string")
        if (savedString) setString(savedString)
    }, [])

    let unitsStr = string.split(" ")
    let units = []

    const getUnit = (name = "") => {
        let unitId = unitsHashMap[name]
        if (unitId === undefined) unitId = unitsHashMap[name.toLowerCase()]
        return unitData.units[unitId]
    }

    if (string) {
        for (const unitStr of unitsStr) {
            try {
                let tier = unitStr.match(/[Tt]([1-6])/)
                tier = tier ? tier[1] : 0

                let count = unitStr.match(/\*([0-9]*)/)
                count = count ? parseInt(count[1]) : 1

                let magicImmune = !!unitStr.match(/\(MI\)/)
                let physImmune = !!unitStr.match(/\(PI\)/)

                let senior = !!unitStr.match("Sr")

                let name = unitStr.replace(`T${tier}`, "").replace(`t${tier}`, "")
                name = name.replace(`*${count}`, "")
                name = name.replace("(MI)", "")
                name = name.replace("(PI)", "")
                if (senior) name = name.replace(/^Sr/, "")

                if (tier) senior = true

                let elite = Math.max(0, tier - 3)
                tier -= elite

                let unitInfo = getUnit(name)
                let star = unitInfo.star
                name = unitInfo.names[0]

                if (senior) star++

                units.push({
                    name: name,
                    star: star,
                    tier: tier,
                    elite: elite,
                    count: count,
                    magicImmune: magicImmune,
                    physImmune: physImmune,
                    local: unitInfo.local
                })
            } catch (error) {}
        }
    }

    return (
        <div className={styles.unitsBody}>
            <Inputs setString={changeString} setScale={changeScale} scale={scale} string={string} />
            {string && units.length ? <DownloadImage /> : <></>}
            {string && units.length ? <UnitImages units={units} scale={scale} /> : <></>}
            <p className={styles.gray}>
                If you like the project, you can star it on{" "}
                <a
                    className={styles.blue}
                    href="https://github.com/coldfeudal/Endless-Frontier-Text2Units"
                    target="_blank"
                    rel="noreferrer"
                >
                    github
                </a>
            </p>

            {/* <>
                <div className={styles.inputs}>
                    <div className={styles.title}>Result JSON</div>
                    <pre
                        style={{
                            fontSize: "16px",
                            padding: "20px",
                            border: "1px solid black",
                            width: "80vw"
                        }}
                    >
                        {JSON.stringify(units, null, 4)}
                    </pre>
                </div>
            </> */}
        </div>
    )
}

const DownloadImage = () => {
    return (
        <div>
            <div
                className={styles.download}
                download="EF_Converted.png"
                onClick={(e) => {
                    toPng(document.querySelector(`.${styles.unitsInner}`)).then((img) => {
                        download(img, "EF_Units.png", "image/png")
                    })
                }}
            >
                Download Image
            </div>
        </div>
    )
}

const Inputs = ({ setString = () => {}, setScale = () => {}, scale = 1, string = "" }) => {
    return (
        <div className={styles.inputs}>
            <div className={styles.title}>Controls</div>
            <div className={styles.inputLines}>
                <div className={styles.inputLine}>
                    <div className={styles.label}>Unit string:</div>
                    <input
                        type="text"
                        value={string}
                        className={styles.input}
                        onChange={(e) => {
                            setString(e.target.value)
                        }}
                        placeholder="E.g. SrDK(PI) T3Gunner*3 T6DK(MI) Gunner"
                    />
                </div>
                <div className={styles.inputLine}>
                    <div className={styles.label}>Scale:</div>
                    <div className={styles.inputFlex}>
                        <input
                            type="range"
                            min=".1"
                            max="10"
                            step=".1"
                            value={scale}
                            className={styles.input}
                            onChange={(e) => {
                                setScale(e.target.value)
                            }}
                        />
                        <input
                            type="number"
                            min=".1"
                            max="10"
                            step=".1"
                            value={scale}
                            className={`${styles.input} ${styles.number}`}
                            onChange={(e) => {
                                setScale(e.target.value)
                            }}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}

const UnitImages = ({ units = [], scale = 1 }) => {
    const [fixerHeight, setFixerHeight] = useState(0)

    useEffect(() => {
        let imageObj = document.querySelector(`.${styles.units}`)
        setFixerHeight(imageObj.getBoundingClientRect().height)
    }, [scale, units])

    let i = 0
    let cols = 6
    let allCount = Object.keys(units).reduce(function (previous, key) {
        return previous + units[key].count
    }, 0)

    return (
        <div className={styles.unitsWrapper}>
            <div
                className={styles.heightFixer}
                style={{
                    height: `${fixerHeight}px`
                }}
            ></div>

            <div
                className={styles.units}
                style={{
                    transform: `scale(${scale})`
                }}
            >
                <div
                    className={styles.unitsInner}
                    style={{
                        gridTemplateColumns: `repeat(${Math.min(allCount, cols)}, 1fr)`
                    }}
                >
                    {units.map((unit) => {
                        return [...Array(unit.count)].map((e, n) => {
                            return (
                                <div
                                    key={i++}
                                    className={`${styles.unit} ${styles[`star-${unit.star}`]}`}
                                >
                                    <div className={styles.unitImage}>
                                        <div
                                            className={styles.unitImageInner}
                                            style={{
                                                backgroundImage: `url('/${
                                                    unit.senior ? "senior" : "normal"
                                                }/${unit.name}.png')`
                                            }}
                                        ></div>
                                    </div>
                                    <div className={styles.tier}>
                                        {[...Array(unit.tier)].map((e, i) => {
                                            return (
                                                <div
                                                    key={i}
                                                    className={styles.tierImage}
                                                    style={{
                                                        top: `${-6.5 * styles.tierSizeMult * i}px`
                                                    }}
                                                ></div>
                                            )
                                        })}
                                    </div>
                                    <div
                                        className={styles.elite}
                                        style={{
                                            gridTemplateColumns: `repeat(${unit.elite}, 1fr)`
                                        }}
                                    >
                                        {[...Array(unit.elite)].map((e, i) => {
                                            return <div key={i} className={styles.eliteImage}></div>
                                        })}
                                    </div>
                                    <div className={`${styles.immune}`}>
                                        {unit.magicImmune ? (
                                            <div className={styles.magic}></div>
                                        ) : (
                                            <></>
                                        )}
                                        {unit.physImmune ? (
                                            <div className={styles.phys}></div>
                                        ) : (
                                            <></>
                                        )}
                                    </div>
                                </div>
                            )
                        })
                    })}
                </div>
            </div>
        </div>
    )
}

export default Units
