import { Box, CircularProgress, Typography } from "@mui/material";
import { useForm } from "react-hook-form";
import { InputField } from "../components/InputField";
import { ButtonClick } from "../components/ButtonClick";
import flaskIcon from "../assets/flask-4.svg";
import { useState } from "react";

function MainForm() {

    const {
        register,
        handleSubmit,
        formState: { errors },
        setValue,
        watch,
        setError
    } = useForm();

    const [loading, setLoading] = useState(false);
    const [errorMessage, setErrorMessage] = useState(null);

    const onSubmit = async (data) => {
        setLoading(true);
        setErrorMessage(null);

        // Собираем payload для API
        const payload = {
            ...data,
            drug_info: {
                drug_name: data.drug_name,
                active_substance: data.active_substance,
                dosage_form: data.dosage_form,
                dosage: data.dosage // <-- добавь поле
            }
        };

        // Убираем поля верхнего уровня, которые теперь внутри drug_info
        delete payload.drug_name;
        delete payload.active_substance;
        delete payload.dosage_form;
        delete payload.dosage;

        try {
            const response = await fetch(
                "https://d5dlr1b0vg46tlm11rq7.yl4tuxdu.apigw.yandexcloud.net/generate",
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload),
                }
            );

            if (!response.ok) {
                const text = await response.text();
                throw new Error(text);
            }
            
            const blob = await response.blob();

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "inclusion_criteria.docx";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);

        } catch (error) {
            console.error("Ошибка:", error);
            setErrorMessage("Не удалось сформировать отчёт. Проверьте соединение.");
        } finally {
            setLoading(false);
        }
    };

    return(
        <div className="container" >
            <form
                onSubmit={handleSubmit(onSubmit)}
                noValidate
                autoComplete="off"
            >
                <Box sx={{ display: "flex", justifyContent: "center" }}>
                    <img
                        src={flaskIcon}
                        alt="Flask icon"
                        style={{
                            width: "180px",
                            marginBottom: "14px",
                        }}
                    />
                </Box>
                <Typography
                    variant="h3"
                    align="center"
                    sx={{ fontWeight: 700, mb: 1, color: "var(--orange-primary)" }}
                >
                    Aspectus
                </Typography>

                <Typography
                    variant="h5"
                    align="center"
                    sx={{ fontWeight: "bold", mb: 2}}
                >
                    Введите данные:
                </Typography>

                    {/* ---------- ОБЩАЯ ИНФОРМАЦИЯ ---------- */}
                    <Typography
                        variant="h6"
                        sx={{ mt: 2, mb: 2, fontWeight: 600, color: "var(--orange-secondary)" }}
                    >
                        Общая информация о протоколе
                    </Typography>

                    <InputField 
                        label="ID протокола" 
                        placeholder="Введите ID протокола" 
                        type="number" 
                        register={register("protocol_id", { required: "Обязательное поле" })}
                        error={errors.protocol_id}
                    />

                    <InputField
                        label="Название спонсора" 
                        placeholder="Введите название спонсора" 
                        type="text" 
                        register={register("sponsor_name", { required: "Обязательное поле" })}
                        error={errors.sponsor_name}
                    />

                    <InputField
                        label="Исследовательский центр" 
                        placeholder="Введите название центра" 
                        type="text" 
                        register={register("study_center", { required: "Обязательное поле" })}
                        error={errors.study_center}
                    />

                    <InputField
                        label="Биоаналитическая лаборатория" 
                        placeholder="Введите название лаборатории" 
                        type="text" 
                        register={register("bioanalytical_lab_name", { required: "Обязательное поле" })}
                        error={errors.bioanalytical_lab_name}
                    />

                    {/* ---------- ПРЕПАРАТ ---------- */}
                    <Typography
                        variant="h6"
                        sx={{ mt: 4, mb: 2, fontWeight: 600, color: "var(--orange-secondary)" }}
                    >
                        Информация об исследуемом препарате
                    </Typography>

                    <InputField
                        label="Название препарата" 
                        placeholder="Введите название препарата" 
                        type="text" 
                        register={register("drug_name", { required: "Обязательное поле" })}
                        error={errors.drug_name}
                    />

                    <InputField
                        label="Действующее вещество" 
                        placeholder="Введите действующее вещество" 
                        type="text" 
                        register={register("active_substance", { required: "Обязательное поле" })}
                        error={errors.active_substance}
                    />

                    <InputField
                        label="Лекарственная форма" 
                        placeholder="Введите лекарственную форму" 
                        type="text" 
                        register={register("dosage_form", { required: "Обязательное поле" })}
                        error={errors.dosage_form}
                    />

                    <InputField
                        label="Дозировка (мг)"
                        placeholder="Введите дозировку"
                        type="number"
                        register={register("dosage", { required: "Обязательное поле" })}
                        error={errors.dosage}
                    />

                    {/* ---------- ПАРАМЕТРЫ ИССЛЕДОВАНИЯ ---------- */}
                    <Typography
                        variant="h6"
                        sx={{ mt: 4, mb: 2, fontWeight: 600, color: "var(--orange-secondary)" }}
                    >
                        Характеристики добровольцев
                    </Typography>

                    <InputField
                        label="Допустимый пол"
                        placeholder="Выберите пол"
                        type="text"
                        register={register("gender_allowed", { required: "Обязательное поле" })}
                        error={errors.gender_allowed}
                        options={["Не важно", "Мужской", "Женский"]}
                    />

                    <InputField
                        label="Необходимый интервал после предыдущего исследования (мес.)" 
                        placeholder="Введите количество месяцев" 
                        type="number" 
                        register={register("prior_study_exclusion_months", { required: "Обязательное поле" })}
                        error={errors.prior_study_exclusion_months}
                    />

                    <Box sx={{ mt: 4, display: "flex", justifyContent: "center" }}>
                        <ButtonClick
                            label={
                                loading ? (
                                    <>
                                        <CircularProgress size={20} sx={{ color: "white", mr: 1 }} />
                                        Формирование...
                                    </>
                                ) : (
                                    "Сформировать черновик отчета"
                                )
                            }
                            type="submit"
                            color="var(--orange-primary)"
                            colorHover="var(--orange-secondary)"
                            colorText="white"
                            disabled={loading}
                        />
                    </Box>

            </form>
        </div>
    )
}

export default MainForm