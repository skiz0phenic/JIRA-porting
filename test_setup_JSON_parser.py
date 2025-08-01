import json
'''
default core list: core_os or core (if core_os is not present)
tifs_image_list
sbl_image_list
appimage_list
constraint_string
uart I/O_dict
{
expected_string_in_uart_logs
uart_input
timeout
}
'''


def test_setup_JSON_parser(json_extracted_test_setup,jira_timeout,PLATFORM):
    common_params=json_extracted_test_setup["common_params"]
    #print(common_params)
    PLATFORM_params={}
    if(PLATFORM in json_extracted_test_setup.keys()):
        PLATFORM_params=json_extracted_test_setup[PLATFORM]
    #print(PLATFORM_params)
    final_params={
        "core_list":None,
        "tifs_image_list":None,
        "sbl_image_list":None,
        "appimage_list":None,
        "uart_list_of_dict":None,
        "constraint_dict":None,
    }

    #fill up final_params from PLATFORM_params

    #extracting core_list
    if(PLATFORM in final_params.keys()):
        if("core_os" in PLATFORM_params.keys()):
            final_params["core_list"]=PLATFORM_params["core_os"]
        elif("core" in PLATFORM_params.keys()):
            final_params["core_list"]=PLATFORM_params["core"]
        else:
            final_params["core_list"]=None
        #print("core list is ",final_params["core_list"])

        #extracting tifs_image_list
        if("tifs_image" in PLATFORM_params.keys()):
            final_params["tifs_image_list"]=[]
            i=1
            key="image"+str(i)
            while(key in PLATFORM_params["tifs_image"].keys()):
                final_params["tifs_image_list"].append(PLATFORM_params["tifs_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
        else:
            final_params["tifs_image_list"]=None        
        #print("tifs_image list is ",final_params["tifs_image_list"])
        #extracting sbl_image_list
        if("sbl_image" in PLATFORM_params.keys()):
            final_params["sbl_image_list"]=[]
            i=1
            key="image"+str(i)
            while(key in PLATFORM_params["sbl_image"].keys()):
                final_params["sbl_image_list"].append(PLATFORM_params["sbl_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
        else:
            final_params["sbl_image_list"]=None
        #print("sbl_image list is ",final_params["sbl_image_list"])

        #extracting appimage_list
        if("app_image" in PLATFORM_params.keys()):
            final_params["appimage_list"]=[]
            i=1
            key="image"+str(i)
            while(key in PLATFORM_params["app_image"].keys()):
                final_params["appimage_list"].append(PLATFORM_params["app_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
        else:
            final_params["appimage_list"]=None
        #print("appimage list is ",final_params["appimage_list"])

        #extracting uart_list_of_dict will do with common_params
        if("uart_input" in PLATFORM_params.keys()):
            final_params["uart_list_of_dict"]=[]
            current_dict={}
            i=1
            key="uart_input_"+str(i)
            while(key in PLATFORM_params["uart_input"].keys()):
                current_dict["expected_string_in_uart_logs"]=PLATFORM_params["uart_input"][key]["constraint"]
                current_dict["uart_input"]=PLATFORM_params["uart_input"][key]["message"]
                current_dict["timeout"]=PLATFORM_params["uart_input"][key]["timeout"]
                final_params["uart_list_of_dict"].append(current_dict)
                i+=1
                key="uart_input_"+str(i)
        else:
            pass
        #print("uart_list_of_dict is ",final_params["uart_list_of_dict"])
        #extracting constraint_list
        if("constraint" in PLATFORM_params.keys()):
            final_params["constraint_dict"]=[]
            i=1
            key="constraint_"+str(i)
            while(key in PLATFORM_params["constraint"].keys()):
                final_params["constraint_dict"].append(PLATFORM_params["constraint"][key])
                i+=1
                key="constraint_"+str(i)
        else:
            final_params["constraint_dict"]=None
        #print("constraint list is ",final_params["constraint_dict"])

    #fill up final_params from common_params only if some key is None i.e its not present in PLATFORM_params
    #extracting core_list
    if(final_params["core_list"] is None):
        if("core_os" in common_params.keys()):
            final_params["core_list"]=PLATFORM_params["core_os"]
        elif("core" in common_params.keys()):
            final_params["core_list"]=common_params["core"]
        else:
            final_params["core_list"]=None
        #print("updating_core list is ",final_params["core_list"])
    
    #extracting tifs_image_list
    if(final_params["tifs_image_list"] is None):
        if("tifs_image" in common_params.keys()):
            final_params["tifs_image_list"]=[]
            i=1
            key="image"+str(i)
            while(key in common_params["tifs_image"].keys()):
                final_params["tifs_image_list"].append(common_params["tifs_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
        else:
            final_params["tifs_image_list"]=None
        #print("updating_tifs_image list is ",final_params["tifs_image_list"])

    #extracting sbl_image_list
    if(final_params["sbl_image_list"] is None):
        if("sbl_image" in common_params.keys()):
            final_params["sbl_image_list"]=[]
            i=1
            key="image"+str(i)
            while(key in common_params["sbl_image"].keys()):
                final_params["sbl_image_list"].append(common_params["sbl_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
        else:
            final_params["sbl_image_list"]=None
        #print("updating_sbl_image list is ",final_params["sbl_image_list"])

    #extracting appimage_list
    if(final_params["appimage_list"] is None):
        if("app_image" in common_params.keys()):
            final_params["appimage_list"]=[]
            i=1
            key="image"+str(i)
            while(key in common_params["app_image"].keys()):
                final_params["appimage_list"].append(common_params["app_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
        else:
            final_params["appimage_list"]=None
        #print("updating_appimage list is ",final_params["appimage_list"])
    
    #extracting uart_list_of_dict
    if(final_params["uart_list_of_dict"] is None):
        if("uart_input" in common_params.keys()):
            final_params["uart_list_of_dict"]=[]
            current_dict={}
            i=1
            key="uart_input_"+str(i)
            while(key in common_params["uart_input"].keys()):
                current_dict["expected_string_in_uart_logs"]=common_params["uart_input"][key]["constraint"]
                current_dict["uart_input"]=common_params["uart_input"][key]["message"]
                current_dict["timeout"]=common_params["uart_input"][key]["timeout"]
                final_params["uart_list_of_dict"].append(current_dict)
                i+=1
                key="uart_input_"+str(i)
        else:
            pass
        #print("updating_uart_list is ",final_params["uart_list_of_dict"])
    #extracting constraint_list
    if(final_params["constraint_dict"] is None):
        if("constraint" in common_params.keys()):
            final_params["constraint_dict"]=[]
            i=1
            key="constraint_"+str(i)
            while(key in common_params["constraint"].keys()):
                final_params["constraint_dict"].append(common_params["constraint"][key])
                i+=1
                key="constraint_"+str(i)
        else:
            pass
        #print("updating_constraint_list is ",final_params["constraint_dict"])
        #print(json.dumps(final_params,indent=4))
    return final_params  

jira_test_setup="""{
    "am62xx-sk-lp-hsfs": {
        "scripts": "generic_json_cfg.py",
        "core": [
            "mcu0_0"
        ],
        "tifs_image": {
            "image1": {
                "image_path": "pdk*/packages/ti/drv/sciclient/soc/V2/tifs.bin"
            }
        },
        "sbl_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/tools/boot/sbl_prebuilt/am62x-sk-lp/sbl_uart.release.hs_fs.tiimage"
            }
        },
        "app_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/examples/hello_world/am62x-sk-lp/m4fss0-0_nortos/ti-arm-clang/hello_world.release.appimage.hs_fs"
            },
            "image2": {
                "image_path": "mcu_plus_sdk*/mcal/binary/config_1/mcal_test_dio_config_1/bin/am62x-evm/mcal_test_dio_config_1_mcu0_0_release.appimage.hs_fs"
            }
        },
        "constraint": {
            "constraint_1": {
                "message": "All tests have passed",
                "log_port": "mpu2"
            }
        }
    },
    "am62ax-sk-hsfs": {
        "scripts": "generic_json_cfg.py",
        "core": [
            "mcu0_0"
        ],
        "sbl_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/tools/boot/sbl_prebuilt/am62ax-sk/sbl_uart.release.hs_fs.tiimage"
            }
        },
        "app_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/mcal/binary/config_1/mcal_test_dio_config_1/bin/am62ax-evm/mcal_test_dio_config_1_mcu0_0_release.appimage.hs_fs"
            },
            "image2": {
                "image_path": "mcu_plus_sdk*/examples/hello_world/am62ax-sk/r5fss0-0_freertos/ti-arm-clang/hello_world.release.appimage.hs_fs"
            }
        },
        "constraint": {
            "constraint_1": {
                "message": "All tests have passed",
                "log_port": "mpu3"
            }
        }
    },
    "am62dx-evm-hsfs": {
        "scripts": "generic_json_cfg.py",
        "core": [
            "mcu0_0"
        ],
        "sbl_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/tools/boot/sbl_prebuilt/am62dx-evm/sbl_uart.release.hs_fs.tiimage"
            }
        },
        "app_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/mcal/binary/config_1/mcal_test_dio_config_1/bin/am62dx-evm/mcal_test_dio_config_1_mcu0_0_release.appimage.hs_fs"
            },
            "image2": {
                "image_path": "mcu_plus_sdk*/examples/hello_world/am62dx-evm/r5fss0-0_freertos/ti-arm-clang/hello_world.release.appimage.hs_fs"
            }
        },
        "constraint": {
            "constraint_1": {
                "message": "All tests have passed",
                "log_port": "mcu2"
            }
        }
    },
    "am275x-evm": {
        "scripts": "generic_json_cfg.py",
        "core_os": [
            "r5fss0-0_nortos"
        ],
        "sbl_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/tools/boot/sbl_prebuilt/am275x-evm/sbl_uart.release.hs_fs.tiimage"
            }
        },
        "app_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/mcal/binary/config_1/mcal_test_dio_config_1/bin/am275x-evm/mcal_test_dio_config_1_mcu0_0_release.mcelf.hs_fs"
            }
        },
        "constraint": {
            "constraint_1": {
                "message": "All tests have passed",
                "log_port": "mcu2"
            }
        }
    },
    "j7200-evm": {
        "tifs_image": {
            "image1": {
                "image_path": "pdk*/packages/ti/drv/sciclient/soc/V2/tifs.bin"
            }
        }
    },
    "j721s2-evm": {
        "tifs_image": {
            "image1": {
                "image_path": "pdk*/packages/ti/drv/sciclient/soc/V4/tifs.bin"
            }
        }
    },
    "j784s4-evm": {
        "tifs_image": {
            "image1": {
                "image_path": "pdk*/packages/ti/drv/sciclient/soc/V6/tifs.bin"
            }
        },
        "sbl_image": {
            "image1": {
                "image_path": "pdk*/packages/ti/boot/sbl/binary/{platform_info.platform}/uart/bin/sbl_uart_img_mcu1_0_release.tiimage"
            }
        },
        "app_image": {
            "image1": {
                "image_path": "pdk*/mcal/binary/config_1/mcal_test_dio_config_1/bin/{platform_info.platform}/mcal_test_dio_config_1_{core}_release.appimage"
            }
        }
    },
    "j721e-evm": {
        "tifs_image": {
            "image1": {
                "image_path": "pdk*/packages/ti/drv/sciclient/soc/V1/tifs.bin"
            }
        }
    },
    "common_params": {
        "boot_os": "baremetal",
        "core": [
            "mcu1_0"
        ],
        "iteration": "1",
        "scripts": "mcal_test.py",
        "test_app_name": "mcal_test_dio_config_1",
        "boot_mode": "uart",
        "skip_duplicate": "true",
        "sbl_image": {
            "image1": {
                "image_path": "pdk*/packages/ti/boot/sbl/binary/{platform_info.platform}/uart/bin/sbl_uart_img_mcu1_0_release.tiimage"
            }
        },
        "app_image": {
            "image1": {
                "image_path": "pdk*/mcal/binary/config_1/mcal_test_dio_config_1/bin/{platform_info.platform}/mcal_test_dio_config_1_{core}_release.appimage"
            }
        },
        "constraint": {
            "constraint_1": {
                "message": "All tests have passed",
                "port": "mcu1"
            }
        },
        "uart_input": {
            "uart_input_1": {
                "constraint": "Enter Choice:",
                "timeout": 30,
                "message": "Enter Choice successful",
                "depends_prev": "false",
                "port": "mcu1",
                "send_command_with_newline": 1,
                "command": "3"
            }
        }
    },
    "am62px-sk-lp-hsfs": {
        "scripts": "generic_json_cfg.py",
        "core": [
            "mcu0_0"
        ],
        "sbl_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/tools/boot/sbl_prebuilt/am62px-sk/sbl_uart.release.hs_fs.tiimage"
            }
        },
        "app_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/mcal/binary/config_1/mcal_test_dio_config_1/bin/am62px-evm/mcal_test_dio_config_1_mcu0_0_release.appimage.hs_fs"
            },
            "image2": {
                "image_path": "mcu_plus_sdk*/examples/drivers/ipc/ipc_rpmsg_echo/am62px-sk/wkup-r5fss0-0_freertos/ti-arm-clang/ipc_rpmsg_echo.release.appimage.hs_fs"
            }
        },
        "constraint": {
            "constraint_1": {
                "message": "All tests have passed",
                "log_port": "mpu3"
            }
        }
    },
    "j722s-hsfsevm": {
        "scripts": "generic_json_cfg.py",
        "core": [
            "mcu0_0"
        ],
        "sbl_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/tools/boot/sbl_prebuilt/j722s-evm/sbl_uart.release.hs_fs.tiimage"
            }
        },
        "app_image": {
            "image1": {
                "image_path": "mcu_plus_sdk*/mcal/binary/config_1/mcal_test_dio_config_1/bin/j722s-evm/mcal_test_dio_config_1_mcu0_0_release.appimage.hs_fs"
            }
        },
        "constraint": {
            "constraint_1": {
                "message": "All tests have passed",
                "log_port": "mpu1"
            }
        }
    },
    "j742s2-hsfsevm": {
        "tifs_image": {
            "image1": {
                "image_path": "pdk*/packages/ti/drv/sciclient/soc/V6/tifs.bin"
            }
        },
        "sbl_image": {
            "image1": {
                "image_path": "pdk*/packages/ti/boot/sbl/binary/j742s2-evm/uart/bin/sbl_uart_img_mcu1_0_release.tiimage"
            }
        },
        "app_image": {
            "image1": {
                "image_path": "pdk*/mcal/binary/config_1/mcal_test_dio_config_1/bin/j742s2-evm/mcal_test_dio_config_1_{core}_release.appimage"
            }
        }
    }
}"""
jira_test_setup_json_check = jira_test_setup.replace("\n", "").replace("\r", "").strip()
json_extracted_test_setup = json.loads(jira_test_setup_json_check)
#print(json_extracted_test_setup)
test_setup_JSON_parser(json_extracted_test_setup,600,"am62s")

