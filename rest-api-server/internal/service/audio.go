package service

type IAudioRepository interface {
	CreateAudioDb()
	UploadAudioS3()
	DownloadSummaryS3()
	AddDataToMsgBroker()
}

type AudioService struct {
	repo IAudioRepository
}

func NewAudioService(repo IAudioRepository) *AudioService {
	return &AudioService{
		repo: repo,
	}
}

func (s *AudioService) Upload() {

}
func (s *AudioService) Download() {

}
