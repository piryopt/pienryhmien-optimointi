import { useTranslation } from "react-i18next"
import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import * as XLSX from "xlsx"
import { useNotification } from "../context/NotificationContext"
import surveyService from "../services/surveys"
import StageDropdown from "../components/survey_answers_page_components/StageDropdown"
import SurveyResultsTable from "../components/survey_results_page_components/SurveyResultsTable"
import Happiness from "../components/survey_results_page_components/Happiness"

const MultistageSurveyResultsPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [surveyResultsData, setSurveyResultsData] = useState(null)
  const [stages, setStages] = useState([])
  const [currStage, setCurrStage] = useState(null)
  const [currResults, setCurrResults] = useState([])
  const [loading, setLoading] = useState(true)

  const [droppedGroups, setDroppedGroups] = useState([])
  const [infoKeys, setInfoKeys] = useState([])
  const [additionalInfos, setAdditionalInfos] = useState([])
  const [happinessData, setHappinessData] = useState([])
  const [resultsSaved, setResultsSaved] = useState(false)
  const [results, setResults] = useState([])

  const { t } = useTranslation()
  const { showNotification } = useNotification()

  useEffect(() => {
    const getSurveyResults = async () => {
      try {
        const response = await surveyService.getSurveyResultsData(id)
        if (!response.stageResults || !Array.isArray(response.stageResults)) {
          navigate(`/surveys/multistage/${id}/answers`, { replace: true })
          setSurveyResultsData(response)
          setStages([])
          setCurrStage(null)
          setCurrResults([])
          return
        }

        setSurveyResultsData(response)
        const surveyStages = response.stageResults.map((stage) => stage["stage"] || null)
        setStages(surveyStages)
        setCurrStage(surveyStages[0] ?? null)
        setCurrResults(response.stageResults[0] ?? null)
      } catch (err) {
          console.error("Error loading survey results", err)
      } finally {
        setTimeout(() => {
          setLoading(false)
        }, 1)
      }
    }
    getSurveyResults()
  }, [])

  useEffect(() => {
    if (!surveyResultsData || !Array.isArray(surveyResultsData.stageResults)) return
    const active =
      surveyResultsData.stageResults.find((s) => s.stage === currStage) ||
      surveyResultsData.stageResults[0] ||
      null
    setCurrResults(active)

    if (active) {
      setResults(active.results || [])
      setDroppedGroups(active.droppedGroups || [])
      setInfoKeys(active.infos || [])
      setAdditionalInfos(active.additionalInfoKeys || {})
      setHappinessData(active.happinessData || [])
      setResultsSaved(Boolean(active.resultsSaved))
    } else {
      setResults([])
      setDroppedGroups([])
      setInfoKeys([])
      setAdditionalInfos([])
      setHappinessData([])
      setResultsSaved(false)
    }
  }, [currStage, surveyResultsData])

  const exportToExcel = () => {
    if (!surveyResultsData || !Array.isArray(surveyResultsData.stageResults) || surveyResultsData.stageResults.length === 0) {
      showNotification(t("Ei tuloksia vietäväksi"), "warning")
      return
    }

    const wb = XLSX.utils.book_new()

    surveyResultsData.stageResults.forEach((stageObj, idx) => {
      const resultsArr = stageObj.results || []
      if (!resultsArr || resultsArr.length === 0) return

      // info key sanitization per stage
      const safeInfoKeys = Array.isArray(stageObj.infos) ? stageObj.infos.filter(k => k && k.info_key) : []
      const additionalInfosPerStage = stageObj.additionalInfoKeys || {}

      const groupData = resultsArr.map((res) => {
        const name = res?.[0]?.[1] ?? ""
        const email = res?.[1] ?? ""
        const groupName = res?.[2]?.[1] ?? ""
        const choiceIndex = (res?.[3] ?? res?.[2]?.[2] ?? "") || ""

        const additional = Object.fromEntries(
          safeInfoKeys
            .map((pair, index) => [pair.info_key, (additionalInfosPerStage?.[res?.[2]?.[0]] || [])[index]])
            .filter(([key, value]) => key && value !== undefined && value !== null && value !== "")
        )

        return {
          [t("Nimi")]: name,
          [t("Sähköposti")]: email,
          [t("Ryhmä")]: groupName,
          [t("Monesko valinta")]: choiceIndex,
          ...additional
        }
      })

      const ws = XLSX.utils.json_to_sheet(groupData)
      const rawName = stageObj.stage || `${t("vaihe")}_${idx + 1}`
      const sheetName = String(rawName).substring(0, 31)
      XLSX.utils.book_append_sheet(wb, ws, sheetName)
    })

    const filename = `${t("tulokset")}_${id || "multivaiheinen"}.xlsx`
    XLSX.writeFile(wb, filename)
  }

  const saveAllResults = () => {
    try {
      surveyService.saveMultistageResults(id)
      showNotification(t("Kaikkien vaiheiden tulokset tallennettu"), "success")
      setResultsSaved(true)
    } catch (err) {
      showNotification(t("Tulosten tallennus epäonnistui"), "error")
      console.error("Error saving all results", err)
    }
  }

  if (loading) return <div>{t("Ladataan...")}</div>

  return (
    <div>
      <h2>{t("Monivaiheisen kyselyn tulokset")}</h2>

      <div style={{ marginTop: "0.5em", marginBottom: "1em" }}>
        <button className="btn btn-outline-primary" onClick={exportToExcel}>
          {t("Vie tulokset Excel-taulukkoon")}
        </button>
        &nbsp;
        {!resultsSaved && (
          <button className="btn btn-outline-success" onClick={saveAllResults}>
            {t("Tallenna kaikkien vaiheiden tulokset")}
          </button>
        )}
      </div>

      <StageDropdown
        stages={stages}
        currStage={currStage}
        setCurrStage={setCurrStage}
      />

      {currResults && (
        <>
          <Happiness average={currResults.happiness} happinessData={happinessData} />
          {droppedGroups && droppedGroups.length > 0 && (
            <div>
              <b style={{ color: "orangered" }}>{t("Ryhmät, jotka pudotettiin jaosta")}</b>
              <ul>
                {droppedGroups.map((group, i) => (
                  <li key={i} style={{ color: "orangered" }}>{group}</li>
                ))}
              </ul>
            </div>
          )}
          <p>
            <b>{t("Opiskelijat on lajiteltu ryhmiin seuraavasti")}:</b>
          </p>

          <SurveyResultsTable results={results} surveyId={id} currStage={currStage} />
        </>
      )}

      {!currResults && <p>{t("Ei tuloksia tälle vaiheelle")}</p>}
    </div>
  )
}  

export default MultistageSurveyResultsPage
